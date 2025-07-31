import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors
from pvlib.iotools import read_epw
import io
import os
import math # Needed for wind speed calculation (log)
import numpy as np # For percentile calculation if needed

# --- Streamlit App Configuration ---
st.set_page_config(layout="wide")

# --- Custom CSS Injection REMOVED ---

st.title("EPW Weather Data Visualization")
st.write("Upload an EPW file to visualize Wind Speed vs. Dry Bulb Temperature.")

# --- Helper Function for Color Conversion ---
def hex_to_rgba(hex_color, alpha=0.2):
    """Converts a hex color string to an RGBA string."""
    try:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 3: hex_color = "".join([c*2 for c in hex_color])
        if len(hex_color) != 6: raise ValueError("Invalid hex color length")
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})'
    except Exception:
        return f'rgba(0, 255, 0, {alpha})' # Fallback to default green

# --- Function to load and cache EPW data ---
@st.cache_data
def load_epw_data(uploaded_file_content):
    """Reads EPW data from uploaded file content."""
    try:
        temp_file_path = "temp_epw_file.epw"
        with open(temp_file_path, "wb") as f: f.write(uploaded_file_content)
        data, meta = read_epw(temp_file_path)
        os.remove(temp_file_path)
        required_columns = ['temp_air', 'wind_speed']
        if not all(col in data.columns for col in required_columns):
            missing = [col for col in required_columns if col not in data.columns]
            st.error(f"EPW file is missing required columns: {missing}"); return None, None
        data = data[required_columns].copy()
        data['temp_air'] = pd.to_numeric(data['temp_air'], errors='coerce')
        data['wind_speed'] = pd.to_numeric(data['wind_speed'], errors='coerce')
        data.dropna(subset=['temp_air', 'wind_speed'], inplace=True)
        return data, meta
    except Exception as e:
        st.error(f"Error reading or parsing EPW file: {e}")
        if os.path.exists("temp_epw_file.epw"): os.remove("temp_epw_file.epw")
        return None, None

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose an EPW file", type="epw")

if uploaded_file is not None:
    epw_content = uploaded_file.getvalue()
    df_weather, metadata = load_epw_data(epw_content)

    if df_weather is not None and not df_weather.empty:
        st.success(f"Successfully loaded EPW data for: {metadata.get('city', 'Unknown Location')}")

        # --- Initialize Session State for Axis Limits (if not already done) ---
        if 'x_min_limit' not in st.session_state:
            x_min_data, x_max_data = float(df_weather['temp_air'].min()), float(df_weather['temp_air'].max())
            y_min_data_orig, y_max_data_orig = float(df_weather['wind_speed'].min()), float(df_weather['wind_speed'].max())
            x_buffer = max((x_max_data - x_min_data) * 0.05, 1.0)
            y_buffer_orig = max((y_max_data_orig - y_min_data_orig) * 0.05, 0.5)
            st.session_state.x_min_limit = float(round(x_min_data - x_buffer))
            st.session_state.x_max_limit = float(round(x_max_data + x_buffer))
            st.session_state.y_min_limit = max(0.0, round(y_min_data_orig - y_buffer_orig, 1))
            st.session_state.y_max_limit = round(y_max_data_orig + y_buffer_orig, 1)
            st.session_state.x_slider_range = (st.session_state.x_min_limit, st.session_state.x_max_limit)
            st.session_state.y_slider_range = (st.session_state.y_min_limit, st.session_state.y_max_limit)

        # --- Callback Functions for Axis Limit Sync ---
        def update_axis_limits_from_slider(axis):
            if axis == 'x': st.session_state.x_min_limit = st.session_state.x_slider_key[0]; st.session_state.x_max_limit = st.session_state.x_slider_key[1]
            elif axis == 'y': st.session_state.y_min_limit = st.session_state.y_slider_key[0]; st.session_state.y_max_limit = st.session_state.y_slider_key[1]

        def update_axis_limits_from_input():
             st.session_state.x_slider_range = (st.session_state.x_min_limit, st.session_state.x_max_limit)
             st.session_state.y_slider_range = (st.session_state.y_min_limit, st.session_state.y_max_limit)

        # --- Sidebar Controls ---
        st.sidebar.header("Plot Customization")

        # --- Expander for Axis Limits --- (Default Closed)
        with st.sidebar.expander("Axis Limits", expanded=False):
            x_min_data, x_max_data = float(df_weather['temp_air'].min()), float(df_weather['temp_air'].max())
            y_min_data_orig, y_max_data_orig = float(df_weather['wind_speed'].min()), float(df_weather['wind_speed'].max())
            x_buffer_large = max((x_max_data - x_min_data) * 0.1, 5.0); y_buffer_large = max((y_max_data_orig - y_min_data_orig) * 0.1, 2.0)
            slider_x_min = float(round(x_min_data - x_buffer_large)); slider_x_max = float(round(x_max_data + x_buffer_large))
            slider_y_min = 0.0; slider_y_max = float(round(y_max_data_orig + y_buffer_large + 20))
            st.slider("Temperature Range (°C) - Drag", min_value=slider_x_min, max_value=slider_x_max, value=st.session_state.x_slider_range, step=0.5, key="x_slider_key", on_change=update_axis_limits_from_slider, args=('x',))
            st.slider("Wind Speed Range (m/s) - Drag", min_value=slider_y_min, max_value=slider_y_max, value=st.session_state.y_slider_range, step=0.1, key="y_slider_key", on_change=update_axis_limits_from_slider, args=('y',))
            col1, col2 = st.columns(2)
            with col1:
                st.number_input("Temp Min (°C)", step=0.5, key="x_min_limit", on_change=update_axis_limits_from_input)
                st.number_input("Wind Min (m/s)", min_value=0.0, step=0.1, key="y_min_limit", on_change=update_axis_limits_from_input)
            with col2:
                st.number_input("Temp Max (°C)", step=0.5, key="x_max_limit", on_change=update_axis_limits_from_input)
                st.number_input("Wind Max (m/s)", min_value=0.0, step=0.1, key="y_max_limit", on_change=update_axis_limits_from_input)

        # --- Expander for Wind Speed Height Adjustment ---
        with st.sidebar.expander("Wind Speed Height Adjustment", expanded=False):
            enable_wind_adjustment = st.toggle("Enable Adjustment", value=False, key="wind_adjust_toggle", help="Adjust wind speed based on height difference and ground roughness.")
            referenceHeight = st.number_input("Weather Station Ref. Height (m)", min_value=0.1, value=10.0, step=0.1, key="ref_h", disabled=not enable_wind_adjustment)
            desiredHeight = st.number_input("Desired Site Height (m)", min_value=0.1, value=10.0, step=0.1, key="des_h", disabled=not enable_wind_adjustment)
            groundRoughnessStation = st.number_input("Ground Roughness (Station)", min_value=0.001, value=0.03, step=0.001, format="%.3f", key="gr_stat", help="Typical values: Open sea=0.0002, Open terrain=0.03, Suburbs=0.5, City center=1.0+", disabled=not enable_wind_adjustment)
            groundRoughnessSite = st.number_input("Ground Roughness (Site)", min_value=0.001, value=0.03, step=0.001, format="%.3f", key="gr_site", help="Typical values: Open sea=0.0002, Open terrain=0.03, Suburbs=0.5, City center=1.0+", disabled=not enable_wind_adjustment)

        # --- Expander for Comfort Band Settings ---
        with st.sidebar.expander("Comfort Band Settings", expanded=False):
            show_comfort_band = st.toggle("Show Comfort Band", value=True, key="show_comfort_toggle", help="Enable or disable the display of the comfort band and its annotation.")
            disable_comfort_inputs = not show_comfort_band
            comfort_band_min_temp = st.number_input("Min Temp (°C)", value=18.0, step=0.5, key="comfort_min", disabled=disable_comfort_inputs)
            comfort_band_max_temp = st.number_input("Max Temp (°C)", value=32.0, step=0.5, key="comfort_max", disabled=disable_comfort_inputs)
            comfort_band_color_hex = st.color_picker("Band Color", value='#90EE90', key="comfort_color", disabled=disable_comfort_inputs) # Default LightGreen
            comfort_band_alpha = st.slider("Band Opacity", min_value=0.0, max_value=1.0, value=0.25, step=0.05, key="comfort_alpha", disabled=disable_comfort_inputs)
            comfort_band_rgba = hex_to_rgba(comfort_band_color_hex, comfort_band_alpha)
            comfort_annot_align = st.selectbox("Text Alignment:", options=['Center', 'Left', 'Right'], index=0, key="comfort_annot_align_select", help="Set horizontal alignment of the 'Comfort Band' text within the band.", disabled=disable_comfort_inputs)
            comfort_annot_ypos = st.slider("Text Vertical Position:", min_value=0.0, max_value=1.0, value=0.95, step=0.01, key="comfort_annot_ypos_slider", format="%.2f", help="Adjust vertical position of 'Comfort Band' text (relative to plot height).", disabled=disable_comfort_inputs)

        # --- Expander for General Appearance ---
        with st.sidebar.expander("General Appearance", expanded=False):
            selected_chart_bg_color = st.color_picker("Chart Background Color", value='#FFFFFF', key="bg_color_picker", help="Select the background color for the entire chart area (plot and paper). Ignored if background is transparent.")
            selected_font_color = st.color_picker("Text/Font Color", value='#000000', key="font_color_picker", help="Select the color for axis labels/titles, tick labels, and annotations.") # Default Black
            selected_font_size = st.slider("Font Size", min_value=6, max_value=24, value=18, step=1, key="font_size_slider", help="Adjust the size for titles, axis labels, ticks, and annotations.") # Default 18
            transparent_bg = st.toggle("Make Background Transparent", value=False, key="transp_bg_toggle", help="Make both the plot area and the surrounding area transparent (overrides background color choice).") # Default False

        # --- Expander for Statistics Annotations ---
        with st.sidebar.expander("Statistics Annotations", expanded=False):
            annotation_align = st.selectbox("Text Alignment:", options=['Center', 'Left', 'Right'], index=1, key="annot_align_select", help="Set the horizontal position of the Average/Percentile text labels.") # Default Left
            annotation_yshift = st.slider("Text Vertical Shift (pixels):", min_value=-30, max_value=50, value=15, step=1, key="annot_yshift_slider", help="Adjust the vertical distance of the stats text from its line (+ve is above, -ve is below).") # Default 15

        # --- Expander for Marker & Scale ---
        with st.sidebar.expander("Marker & Color Scale", expanded=False):
            preferred_scales = ['jet', 'RdYlBu_r', 'Spectral_r']
            all_scales = px.colors.named_colorscales(); other_scales = [s for s in all_scales if s not in preferred_scales]
            valid_preferred = [s for s in preferred_scales if s in all_scales]; ordered_scales = valid_preferred + other_scales
            try:
                if 'RdYlBu_r' in ordered_scales: default_color_index = ordered_scales.index('RdYlBu_r')
                elif valid_preferred: default_color_index = 0
                else: default_color_index = 0
            except ValueError: default_color_index = 0
            selected_color_scale = st.selectbox("Select Marker Color Scale:", options=ordered_scales, index=default_color_index, key="color_scale_select", help="Controls the color gradient applied to the data points based on temperature.")
            marker_size = st.slider("Marker Size:", min_value=1, max_value=20, value=4, step=1, key="marker_size_slider", help="Adjust the size of the data points (dots).") # Default 4
            use_outline = st.toggle("Outline Markers Only", value=False, key="marker_outline_toggle", help="If activated, only the border of the markers will be colored, the inside will be transparent.")
            outline_width = 1.5 if use_outline else 0.5; filled_marker_line_color = 'rgba(0,0,0,0.4)'
            colorbar_length = st.slider("Color Bar Length (Fraction of Plot Height):", min_value=0.1, max_value=1.0, value=0.8, step=0.05, key="cbar_len_slider", help="Adjust the vertical length of the color bar legend relative to the plot height.") # Default 0.8

        # --- Expander for Plot Dimensions & Export ---
        with st.sidebar.expander("Plot Dimensions & Export", expanded=False):
            plot_width = st.number_input("Plot Width (pixels):", min_value=300, max_value=2000, value=1200, step=50, key="plot_w_input", help="Set the width of the chart on screen in pixels.") # Default 1200
            plot_height = st.number_input("Plot Height (pixels):", min_value=200, max_value=1500, value=900, step=50, key="plot_h_input", help="Set the height of the chart on screen in pixels.") # Default 900
            download_scale = st.slider("Download Image Scale Factor:", min_value=1.0, max_value=10.0, value=4.0, step=0.5, key="dl_scale_slider", help="Increase resolution of downloaded PNG image. Scale=1 is screen resolution. Higher values = larger image file size.") # Default 4.0

        # --- Perform Wind Speed Adjustment ---
        df_plot_data = df_weather.copy(); adjustment_factor = 1.0
        if enable_wind_adjustment:
            valid_inputs = (desiredHeight > 0 and groundRoughnessSite > 0 and referenceHeight > 0 and groundRoughnessStation > 0 and desiredHeight / groundRoughnessSite > 0 and referenceHeight / groundRoughnessStation > 0)
            if valid_inputs:
                 log_arg_num = desiredHeight / groundRoughnessSite; log_arg_den = referenceHeight / groundRoughnessStation
                 if abs(log_arg_den - 1.0) < 1e-9 or abs(math.log(log_arg_den)) < 1e-9 : st.sidebar.warning("Wind adj. failed: Log ratio denominator near zero."); adjustment_factor = 1.0
                 else:
                      log_num = math.log(log_arg_num) if abs(log_arg_num - 1.0) > 1e-9 else 0.0; log_den = math.log(log_arg_den)
                      adjustment_factor = log_num / log_den
                      df_plot_data['wind_speed'] = df_plot_data['wind_speed'] * adjustment_factor; st.sidebar.info(f"Applied wind adj. factor: {adjustment_factor:.3f}")
            else: st.sidebar.warning("Invalid height/roughness values for wind adjustment."); adjustment_factor = 1.0

        # --- Calculate Statistics ---
        comfort_percentage = 0.0
        if not df_plot_data.empty:
            avg_wsp = df_plot_data['wind_speed'].mean(); p95_wsp = df_plot_data['wind_speed'].quantile(0.95)
            comfort_mask = (df_plot_data['temp_air'] >= comfort_band_min_temp) & (df_plot_data['temp_air'] <= comfort_band_max_temp)
            if len(df_plot_data) > 0: comfort_percentage = (comfort_mask.sum() / len(df_plot_data)) * 100
        else: avg_wsp = 0; p95_wsp = 0

        # --- Create Plot ---
        st.subheader("Wind Speed vs. Dry Bulb Temperature")
        fig = go.Figure(data=go.Scattergl(x=df_plot_data['temp_air'], y=df_plot_data['wind_speed'], mode='markers', marker=dict(size=marker_size, line=dict(width=outline_width, color=filled_marker_line_color)), hovertemplate="<b>Time:</b> %{customdata}<br><b>Temp:</b> %{x:.1f} °C<br><b>Wind Speed:</b> %{y:.1f} m/s<extra></extra>", customdata=df_plot_data.index.strftime('%Y-%m-%d %H:%M')))

        # --- Apply Color Styling Conditionally ---
        colorbar_config = dict(title="Temp (°C)", len=colorbar_length, title_font=dict(size=selected_font_size, color=selected_font_color), tickfont=dict(size=selected_font_size, color=selected_font_color))
        if use_outline: fig.update_traces(marker=dict(color='rgba(0,0,0,0)', line=dict(color=df_plot_data['temp_air'], colorscale=selected_color_scale, width=outline_width, cmin=df_plot_data['temp_air'].min(), cmax=df_plot_data['temp_air'].max()), colorscale=selected_color_scale, cmin=df_plot_data['temp_air'].min(), cmax=df_plot_data['temp_air'].max(), showscale=True, colorbar=colorbar_config), selector=dict(mode='markers'))
        else: fig.update_traces(marker=dict(color=df_plot_data['temp_air'], colorscale=selected_color_scale, line=dict(width=outline_width, color=filled_marker_line_color), cmin=df_plot_data['temp_air'].min(), cmax=df_plot_data['temp_air'].max(), showscale=True, colorbar=colorbar_config), selector=dict(mode='markers'))

        # --- Determine Background Colors ---
        if transparent_bg: plot_bg_to_use, paper_bg_to_use = ('rgba(0,0,0,0)', 'rgba(0,0,0,0)')
        else: plot_bg_to_use = selected_chart_bg_color; paper_bg_to_use = selected_chart_bg_color

        # --- Apply Layout Options ---
        fig.update_layout(
            width=plot_width, height=plot_height, xaxis_title='Dry Bulb Temperature (°C)', yaxis_title='Wind Speed (m/s)',
            xaxis_range=[st.session_state.x_min_limit, st.session_state.x_max_limit], yaxis_range=[st.session_state.y_min_limit, st.session_state.y_max_limit],
            font=dict(size=selected_font_size, color=selected_font_color), # Global Default
            xaxis_title_font=dict(size=selected_font_size, color=selected_font_color), yaxis_title_font=dict(size=selected_font_size, color=selected_font_color),
            xaxis_tickfont=dict(size=selected_font_size, color=selected_font_color), yaxis_tickfont=dict(size=selected_font_size, color=selected_font_color),
            plot_bgcolor=plot_bg_to_use, paper_bgcolor=paper_bg_to_use,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        # --- Add Comfort Band Shape (Conditional)---
        actual_comfort_min = min(comfort_band_min_temp, comfort_band_max_temp)
        actual_comfort_max = max(comfort_band_min_temp, comfort_band_max_temp)
        if show_comfort_band:
            fig.add_shape(type="rect", xref="x", yref="paper", x0=actual_comfort_min, y0=0, x1=actual_comfort_max, y1=1, fillcolor=comfort_band_rgba, line_width=0, layer="below")

        # --- Add Lines and Annotations for Stats ---
        if not df_plot_data.empty:
             # Stats Annotations (Average / Percentile)
             x_range_width = st.session_state.x_max_limit - st.session_state.x_min_limit
             annotation_x_stat = st.session_state.x_min_limit; x_anchor_stat = 'left'; x_shift_stat = 10
             if annotation_align == 'Center': annotation_x_stat = st.session_state.x_min_limit + x_range_width * 0.5; x_anchor_stat = 'center'; x_shift_stat = 0
             elif annotation_align == 'Right': annotation_x_stat = st.session_state.x_max_limit; x_anchor_stat = 'right'; x_shift_stat = -10
             annotation_font = dict(size=selected_font_size, color=selected_font_color); annotation_bgcolor = 'rgba(255,255,255,0.6)'
             fig.add_hline(y=avg_wsp, line_dash="dash", line_color=selected_font_color, opacity=0.7)
             fig.add_annotation(x=annotation_x_stat, y=avg_wsp, text=f"Average Wind Speed [{avg_wsp:.1f}] m/s", showarrow=False, yshift=annotation_yshift, font=annotation_font, bgcolor=annotation_bgcolor, xanchor=x_anchor_stat, xshift=x_shift_stat)
             fig.add_hline(y=p95_wsp, line_dash="dot", line_color=selected_font_color, opacity=0.7)
             fig.add_annotation(x=annotation_x_stat, y=p95_wsp, text=f"95th Percentile [{p95_wsp:.1f}] m/s", showarrow=False, yshift=annotation_yshift, font=annotation_font, bgcolor=annotation_bgcolor, xanchor=x_anchor_stat, xshift=x_shift_stat)

             # Comfort Band Annotation (Conditional)
             if show_comfort_band and actual_comfort_max > actual_comfort_min:
                 comfort_annotation_x = actual_comfort_min; comfort_x_anchor = 'left'; comfort_x_shift = 5
                 if comfort_annot_align == 'Center': comfort_annotation_x = actual_comfort_min + (actual_comfort_max - actual_comfort_min) * 0.5; comfort_x_anchor = 'center'; comfort_x_shift = 0
                 elif comfort_annot_align == 'Right': comfort_annotation_x = actual_comfort_max; comfort_x_anchor = 'right'; comfort_x_shift = -5
                 comfort_text = f"Comfort Band<br>{comfort_percentage:.1f}% of the year"
                 fig.add_annotation(x=comfort_annotation_x, yref="paper", y=comfort_annot_ypos, text=comfort_text, showarrow=False, font=annotation_font, bgcolor=annotation_bgcolor, align="center", xanchor=comfort_x_anchor, xshift=comfort_x_shift, yanchor="middle")

        # --- Configure Download Options ---
        config = {'toImageButtonOptions': {'format': 'png', 'filename': f"epw_plot_{metadata.get('city', 'location').replace(' ','_')}", 'height': plot_height, 'width': plot_width, 'scale': download_scale}, 'displaylogo': False}

        # Display plot in Streamlit, passing the config
        st.plotly_chart(fig, use_container_width=False, config=config)

        # --- Optional: Display Data Table ---
        if st.checkbox("Show Filtered Data Table"): st.subheader("Data Points in Plot"); st.dataframe(df_plot_data)

    elif df_weather is not None and df_weather.empty: st.warning("The loaded EPW file contains no valid data rows after processing.")
else: st.info("Awaiting EPW file upload...")