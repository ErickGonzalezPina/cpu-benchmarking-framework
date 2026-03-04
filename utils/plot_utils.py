import os
import matplotlib.pyplot as plt


def create_performance_graph(
    thread_counts: list[int],
    integer_avg_giops: list[float],
    integer_sd_giops: list[float],
    float_avg_gflops: list[float],
    float_sd_gflops: list[float],
    output_file: str,
    process_integer_avg_giops: list[float] | None = None,
    process_integer_sd_giops: list[float] | None = None,
    process_float_avg_gflops: list[float] | None = None,
    process_float_sd_gflops: list[float] | None = None,
    mode_label: str = "threaded",
) -> None:
    '''Create and save a throughput graph with error bars for integer and float benchmarks.'''
    output_directory = os.path.dirname(output_file)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    plt.figure(figsize=(9, 6))

    plt.errorbar(
        thread_counts,
        integer_avg_giops,
        yerr=integer_sd_giops,
        marker="o",
        capsize=5,
        linewidth=2,
        label=f"Integer {mode_label} (GIOPS)",
    )

    plt.errorbar(
        thread_counts,
        float_avg_gflops,
        yerr=float_sd_gflops,
        marker="s",
        capsize=5,
        linewidth=2,
        label=f"Float {mode_label} (GFLOPS)",
    )

    has_process_data = (
        process_integer_avg_giops is not None
        and process_integer_sd_giops is not None
        and process_float_avg_gflops is not None
        and process_float_sd_gflops is not None
    )

    if has_process_data:
        plt.errorbar(
            thread_counts,
            process_integer_avg_giops,
            yerr=process_integer_sd_giops,
            marker="^",
            capsize=5,
            linewidth=2,
            label="Integer process (GIOPS)",
        )

        plt.errorbar(
            thread_counts,
            process_float_avg_gflops,
            yerr=process_float_sd_gflops,
            marker="d",
            capsize=5,
            linewidth=2,
            label="Float process (GFLOPS)",
        )

    title = "CPU Throughput vs Worker Count"
    if has_process_data:
        title = "CPU Throughput vs Worker Count (Threaded vs Process)"

    plt.title(title)
    plt.xlabel("Worker Count")
    plt.ylabel("Throughput (Giga Operations per Second)")
    plt.xticks(thread_counts)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()
