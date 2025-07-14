using CSV, DataFrames, Distributions

data = CSV.read("data.csv", DataFrame)
mem_usage = @allocated begin
    n = nrow(data)
    overall_mean = mean(data.Y)
    groups = groupby(data, :GRUPO)
    k = length(groups)
    SS_between = sum([length(g.Y) * (mean(g.Y) - overall_mean)^2 for g in groups])
    SS_total = sum((data.Y .- overall_mean).^2)
    SS_within = SS_total - SS_between
    df_between = k - 1
    df_within = n - k
    MS_between = SS_between / df_between
    MS_within = SS_within / df_within
    F_value = MS_between / MS_within
    p_value = ccdf(FDist(df_between, df_within), F_value)
    df_anova = DataFrame(
        Source = ["GRUPO", "Residual"],
        DOF = [df_between, df_within],
        Exp_SS = [SS_between, SS_within],
        Mean_Square = [MS_between, MS_within],
        F_value = [F_value, missing],
        Pr = [p_value, missing]
    )
end

CSV.write("resultados_anova_julia.csv", df_anova)

println("MEM_USAGE: $(mem_usage / 1024^2)")