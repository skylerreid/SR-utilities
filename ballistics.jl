function ballistics(v, m, caliber, c_d, rho, crosswind_speed, headwind_speed, target_distance, t_step = 0.01)
    # Convert caliber from inches to meters, then compute cross-sectional area (m²)
    caliber_m = caliber * 0.0254
    csa = π * (caliber_m / 2)^2

    D_forward = 0.5 * rho * c_d * csa
    D_side = 2.5 * D_forward  # more drag sideways

    g = 9.8056
    table = []

    # Initial positions and velocities
    x = 0.0; y = 0.0; z = 0.0; t = 0.0
    v_y = v; v_x = 0.0; v_z = 0.0

    wind_x = crosswind_speed
    wind_y = headwind_speed
    wind_z = 0.0

    for k in 1:100000
        # Relative velocities
        v_rel_x = v_x - wind_x
        v_rel_y = v_y - wind_y
        v_rel_z = v_z - wind_z

        V_rel = sqrt(v_rel_x^2 + v_rel_y^2 + v_rel_z^2)

        #Accelerations
        a_x = -(D_side / m) * v_rel_x * V_rel
        a_y = -(D_forward / m) * v_rel_y * V_rel
        a_z = -(D_forward / m) * v_rel_z * V_rel - g

        #update positions
        x += v_x * t_step
        y += v_y * t_step
        z += v_z * t_step

        #update velocities
        v_x += a_x * t_step
        v_y += a_y * t_step
        v_z += a_z * t_step

        # Store values
        push!(table, [t, y, x, z, v_y, v_x, v_z])
        t += t_step


        # Stop when we reach or exceed target range
        if y >= target_distance
            break
        end
    end

    println("Target distance reached at y = ", y)
    println("Time of flight: ", t)
    println("Total drift (x) at target: ", x)
    println("Total drop (z) at target: ", -z)
    return x, -z, table
end
