import os
import numpy as np
import matplotlib.pyplot as plt
import argparse

def parse_mapping(vtf_path):
    """
    Parse the VSF section to map vtf_id -> particle type (0=real,1=virtual).
    """
    mapping = {}
    with open(vtf_path) as f:
        for line in f:
            if line.startswith('timestep'):
                break
            if line.startswith('atom'):
                parts = line.strip().split()
                vtf_id = int(parts[1])
                name_idx = parts.index('name') + 1
                typ = int(parts[name_idx])
                mapping[vtf_id] = typ
    return mapping

def compute_S_frame(positions, real_ids, virt_ids):
    real_pos = [positions[i] for i in real_ids]
    virt_pos = [positions[i] for i in virt_ids]
    m = []
    for r, v in zip(real_pos, virt_pos):
        d = v - r
        norm = np.linalg.norm(d)
        if norm == 0:
            return None  # skip this frame if the dipole is zero
        m.append(d / norm)
    S_vals = []
    for i in range(3):
        ref = real_pos[i]
        others = [real_pos[j] - ref for j in range(3) if j != i]
        # Avoid division by zero in rhat
        try:
            rhat = [o / np.linalg.norm(o) for o in others]
        except ZeroDivisionError:
            return None
        Ai = (abs(np.dot(m[i], rhat[0])) + abs(np.dot(m[i], rhat[1]))) / 2
        S_vals.append(Ai)
    return sum(S_vals) / 3

def compute_S_for_vtf(vtf_path, segment_lengths):
    mapping = parse_mapping(vtf_path)
    n_atoms = len(mapping)
    real_ids = sorted([i for i, t in mapping.items() if t == 0])
    virt_ids = sorted([i for i, t in mapping.items() if t == 1])
    with open(vtf_path) as f:
        lines = f.readlines()
    frame_starts = [i for i, line in enumerate(lines) if line.startswith('timestep')]
    n_frames = len(frame_starts)
    frame_ranges = []
    for idx in range(n_frames):
        start = frame_starts[idx] + 1
        end = frame_starts[idx + 1] if idx + 1 < n_frames else len(lines)
        frame_ranges.append((start, end))
    init, on1, off1, on2, off2 = segment_lengths
    cum = np.cumsum([0, init, on1, off1, on2, off2])
    off_segments = [('off1', cum[2], off1), ('off2', cum[4], off2)]
    sample_idxs = []
    for name, start_idx, length in off_segments:
        if name == 'off1':
            continue  # skip the first OFF cycle
        third = int(length * 2 / 3)
        for fi in range(start_idx + third, start_idx + length):
            sample_idxs.append(fi)
    S_list = []
    for frame_idx, (s, e) in enumerate(frame_ranges):
        if frame_idx not in sample_idxs:
            continue
        pos = {}
        for line in lines[s:e]:
            parts = line.split()
            if len(parts) < 4:
                continue
            vid = int(parts[0])
            if vid < n_atoms:
                pos[vid] = np.array([float(parts[1]), float(parts[2]), float(parts[3])])
        S_val = compute_S_frame(pos, real_ids, virt_ids)
        if S_val is not None and np.isfinite(S_val):
            S_list.append(S_val)
    return S_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute S and plot histograms P(S) for each shift')
    parser.add_argument('--data-dir', required=True,
                        help='Directory containing trimer_shift_*.vtf files')
    parser.add_argument('--shifts', nargs='+', type=float, required=True,
                        help='List of shift values (e.g. 0.0 0.1 0.2 ...)')
    parser.add_argument('--runs', nargs='+', type=int, default=[1,2,3,4],
                        help='Run indices per shift')
    parser.add_argument('--segment-lengths', nargs=5, type=int,
                        metavar=('initial','on1','off1','on2','off2'),
                        default=[500,100,2000,100,2000],
                        help='Frame counts for each segment')
    parser.add_argument('--bins', type=int, default=50, help='Number of bins for histogram')
    parser.add_argument('--output-dir', default='.', help='Where to save histogram plots')
    args = parser.parse_args()

    shift_S = {sh: [] for sh in args.shifts}
    for sh in args.shifts:
        for run in args.runs:
            fname = os.path.join(args.data_dir, f'trimer_shift_{sh:.1f}_run{run}.vtf')
            if not os.path.exists(fname):
                print(f"File {fname} not found, skipping.")
                continue
            print(f'Processing {fname} ...')
            S_vals = compute_S_for_vtf(fname, args.segment_lengths)
            shift_S[sh].extend(S_vals)

    # Plot histograms robustly
    for sh, S_vals in shift_S.items():
        # Filter out None and NaN values
        S_vals = [v for v in S_vals if v is not None and np.isfinite(v)]
        if not S_vals:
            print(f"Skipping shift {sh} because no valid S values were found.")
            continue
        plt.figure()
        plt.hist(S_vals, bins=args.bins, density=True)
        plt.xlabel('S')
        plt.ylabel('P(S)')
        plt.title(f'Histogram P(S) for shift = {sh:.1f}')
        os.makedirs(args.output_dir, exist_ok=True)
        out_path = os.path.join(args.output_dir, f'hist_shift_{sh:.1f}.png')
        plt.savefig(out_path)
        plt.close()
        print(f'Saved histogram to {out_path}')

    print('All histograms generated.')
