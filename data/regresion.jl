using CSV, DataFrames, GLM, BenchmarkTools, MemPool

# 2. Load data
println("Loading data...")
data_path = "data.csv"
df = try
    CSV.read(data_path, DataFrame)
catch e
    println("Error loading data: ", e)
    exit(1)
end

# Check if required columns exist
required_cols = ["Y", "X1", "X2"]
if !all(col -> col in names(df), required_cols)
    println("Error: Data must contain columns: ", required_cols)
    exit(1)
end

# 3. Run regression with benchmarking
println("\nRunning regression analysis...")

# Benchmark time and memory
bench_result = @benchmark lm(@formula(Y ~ X1 + X2), $df)
mem_usage = @allocated lm(@formula(Y ~ X1 + X2), df)

# 4. Fit model and get results
model = lm(@formula(Y ~ X1 + X2), df)
results = coeftable(model)

# 5. Create comprehensive output DataFrame
output_df = DataFrame(
    Variable = results.rownms,
    Estimate = results.cols[1],
    StdError = results.cols[2],
    tValue = results.cols[3],
    pValue = results.cols[4]
)

# Add performance metrics
performance_df = DataFrame(
    Metric = ["Time (mean)", "Time (min)", "Time (max)", "Memory"],
    Value = [mean(bench_result.times)/1e9,  # Convert to seconds
             minimum(bench_result.times)/1e9,
             maximum(bench_result.times)/1e9,
             mem_usage/1024^2]  # Convert to MB
)

# 6. Save results
println("\nSaving results...")
try
    CSV.write("resultados_regresion_Julia.csv", output_df)
    CSV.write("performance_metrics.csv", performance_df)
    println("Results saved successfully.")
catch e
    println("Error saving results: ", e)
end

# 7. Display summary
println("\n=== Regression Results ===")
println(results)
println("\n=== Performance Metrics ===")
println("Mean time: ", round(mean(bench_result.times)/1e9, digits=4), " s")
println("MEM_USAGE:", round(mem_usage/1024^2, digits=2))
