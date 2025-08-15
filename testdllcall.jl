# Path to your DLL
dll_path = "C:\\Users\\skyle\\OneDrive - Montana State University\\Desktop\\dev\\rolling_avg.dll"

# Example data
data = [1.0, 2.0, 3.0, 4.0, 5.0]
window = 3
out = zeros(length(data) - window + 1)

# Call the DLL function
ccall(
    (:rolling_average, dll_path),  # function name and DLL path
    Cvoid,                        # return type
    (Ptr{Float64}, Csize_t, Csize_t, Ptr{Float64}),  # argument types
    data, length(data), window, out  # arguments
)

println("Rolling average result: ", out)
