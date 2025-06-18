using LibSndFile, FileIO
using FFTW, DSP, Plots

const string_names = ["E2", "A2", "D3", "G3", "B3", "E4"]
const string_freqs = [82.41, 110.00, 146.83, 196.00, 246.94, 329.63] # Hz

function dominant_freq(signal::Vector{Float32}, fs::Real)
    N = length(signal)
    window = hanning(N)
    spectrum = abs.(rfft(signal .* window))
    freqs = range(0, stop=fs/2, length=length(spectrum))
    idx = argmax(spectrum)
    return freqs[idx], freqs, spectrum
end

function closest_string(freq::Float64)
     diffs = abs.(string_freqs .- freq)
     i = argmin(diffs)
     return string_names[i], string_freqs[i], i
end

function analyze_string(filename::String)
    println("🎧 Loading file: $filename")
    audio_buffer = FileIO.load(filename)
    
    y_raw = audio_buffer.data
    fs = audio_buffer.samplerate

    if ndims(y_raw) == 2
        y = Float32.(y_raw[:, 1])
    elseif ndims(y_raw) == 1
        y = Float32.(y_raw)
    else
        error("Unsupported audio data shape after extracting from SampleBuf")
    end

    println("📊 Analyzing...")
    f_detected, freqs, spectrum = dominant_freq(y, fs)
    note, f_expected, _ = closest_string(f_detected)
    diff = round(f_detected - f_expected, digits=2)

    status = abs(diff) < 1 ? "✅ In tune" :
             diff > 0     ? "🔻 Loosen" :
                            "🔺 Tighten"

    println("\n🎵 Closest note: $note")
    println("Detected: $(round(f_detected, digits=2)) Hz")
    println("Expected: $f_expected Hz")
    println("→ $status by $(abs(diff)) Hz")

    # Plot
    p = plot(freqs, spectrum, label="Spectrum", xlabel="Frequency (Hz)", ylabel="Magnitude",
             title="Detected note: $note", legend=:topright,
             xlims=(0, 1000)) # spectrum up to 1000 Hz
    vline!(p, [f_detected], label="Detected: $(round(f_detected, digits=1)) Hz", color=:red, lw=2)
    vline!(p, [f_expected], label="Expected: $(note) = $(f_expected) Hz", color=:green, lw=2, linestyle=:dash)
    display(p)
end