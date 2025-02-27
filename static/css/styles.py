# Define the default theme settings for the app
theme_settings = {
    'primary_color': '#0d5175',
    'secondary_color': '#CEB888',

    'primary_hl_color': '#176a96',
    'secondary_hl_color': '#edd5a1',

    "primary_ll_color": "#0a3c5c",
    "secondary_ll_color": "#ab976d",

    'primary_bg_color': '#212529',
    'secondary_bg_color': '#343c43',
    
    'success_bg_color': '#428a4d',
    'warning_bg_color': '#0a3c5c',

    'primary_low_color': '#3b121c',
    'secondary_low_color': '#54421c',

    'light_font': '#ffffff',
    'dark_font': '#2C2A29',

    'red_band_color': '#ff5733',
    'green_band_color': '#7eff58',
    'blue_band_color': '#05a6fc',

    'switch_width': 35
}

# Define the CSS styles for the app
css = f"""

p {{
    margin-block-start: 0em !important;
    margin-block-end: 0em !important;
}}

a {{
    color: {theme_settings['secondary_color']} !important;
}}

h1,h2,h3 {{
    margin_block_start: 0em !important;
    margin_block_end: 0em !important;
}}

h1 {{
    color: {theme_settings['secondary_color']} !important;
}}

input[type="color"] {{
    margin-top: -10px;
}}


label[for="input"] {{
    background-color: {theme_settings['primary_bg_color']} !important;
    z-index: 2;
}}
  

#input {{
    padding-top: -10px;
}}

input[type="range"] {{
    -webkit-appearance: none;
    width: 100%;
    height: 10px;
    border-radius: 5px;
    background: {theme_settings['primary_bg_color']};
}}

input[type="range"]:active {{
    -webkit-appearance: none;
    width: 100%;
    height: 10px;
    border-radius: 5px;
    background: {theme_settings['primary_bg_color']};
}}


/* Style the thumb in WebKit browsers */
input[type="range"]::-webkit-slider-thumb {{
  -webkit-appearance: none;
  height: 20px;             /* Adjust the size as needed */
  width: 20px;
  border-radius: 50%;       /* This makes it a circle */
  background: {theme_settings['secondary_color']};      /* Change the color or add a background image */
  border: 1px solid #000;   /* Optional: add a border */
  cursor: pointer;
  margin-top: -8px;         /* Align it with the track */
}}

input[type="range"]::-moz-range-thumb {{
  height: 25px;
  width: 25px;
  border-radius: 50%;
  background: #FFFFFF;
  border: 2px solid #000;
  cursor: pointer;
}}

#operations-usage ~ p{{
    color: {theme_settings['dark_font']} !important;
}}

select option:focus,
select option:active,
select option:checked
{{
    background: linear-gradient({theme_settings['primary_color']},{theme_settings['primary_color']});
    background-color: {theme_settings['secondary_color']} !important;
    color: {theme_settings['light_font']} !important;
    text-shadow: none !important;
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
}}

select option:hover {{
    background-color: {theme_settings['primary_ll_color']} !important;
}}


select {{
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
}}

:host, :root {{
    --mdc-theme-primary: {theme_settings['primary_color']} !important;
    --mdc-theme-primary-lightened: {theme_settings['secondary_color']} !important;
    --primary-bg-color: {theme_settings['secondary_bg_color']};
}}

:host .bar {{
    background-color: {theme_settings['primary_color']} !important;
}}

:host .knob {{
    background-color: {theme_settings['primary_low_color']} !important;
}}

:host(.active) .bar {{
    background-color: {theme_settings['secondary_color']} !important; 
    border-color: #ffffff !important;
}}

:host(.active) .knob {{
    background-color: {theme_settings['secondary_low_color']} !important; 
    border-color: #ffffff !important;
}}

.xterm-viewport {{
	width: 340px !important;
	height: 150px !important;
}}

.xterm-helper-textarea {{
    width: 340px !important;
    left: 0px !important;
}}

.xterm-screen {{
	width: 320px !important;
}}

.bk-panel-models-markup-HTML {{
    width: 1500px !important!;
    max_width: 1500px !important;
}}


.main-content {{
    background-color: {theme_settings['secondary_bg_color']} !important;
}}

.mdc-top-app-bar {{
    background: linear-gradient(to right, { theme_settings['primary_color'] }, { theme_settings['primary_ll_color'] }) !important;
}}

.bk-btn-primary {{
    background-color: {theme_settings['secondary_color']} !important;
    color: {theme_settings['dark_font']} !important;
    border: none;
    cursor: pointer;
}}

.bk-btn-primary:hover {{
    background-color: {theme_settings['secondary_ll_color']} !important;
    color: {theme_settings['dark_font']} !important;
    border: none;
    cursor: pointer;
}}

.bk-btn-success {{
    background-color: {theme_settings['primary_color']} !important;
    color: #ffffff !important;
    border: none;
    cursor: pointer;
}}

.bk-btn-success:hover {{
    background-color: {theme_settings['primary_ll_color']} !important;
    color: #ffffff !important;
    border: none;
    cursor: pointer;
}}

.bk-btn a {{
    color: {theme_settings['dark_font']} !important;
}}

.bk-input {{
    background-color: {theme_settings['secondary_bg_color']} !important;
    color: {theme_settings['light_font']} !important;
}}


.bk-tab {{
    padding-top: 20px !important;
    color: {theme_settings['light_font']} !important;
    border-color: #ffffff !important;
}}

.bk-tab:hover {{
    padding-top: 20px !important;
    color: {theme_settings['secondary_hl_color']} !important;
    border-color: #ffffff !important;
}}

.bk-tab.bk-active {{
    color: {theme_settings['secondary_color']} !important;
    border-color: {theme_settings['primary_color']} !important;
    outline: none !important;
}}

.bk-tab:focus {{
  outline: none !important;
}}

.terminal-container {{
    padding-top: 10px;
    max-width: 320px !important;
    box-sizing: border-box;
    scrollbar-color: {theme_settings['primary_hl_color']} {theme_settings['primary_color']};
    }}

::-webkit-scrollbar {{
    width: 12px;  /* Width for vertical scrollbars */
    height: 12px; /* Height for horizontal scrollbars */
}}

::-webkit-scrollbar-track {{
    background-color: {theme_settings['primary_bg_color']} !important;
    border-radius: 10px;
}}

::-webkit-scrollbar-thumb {{
    background-color: {theme_settings['primary_color']} !important;
    border-radius: 10px;
    border: 1px solid {theme_settings['primary_hl_color']};  /* Adds space around the thumb */
}}

.slower, .first, .previous, .reverse, .pause, .play, .next, .last, .faster {{
    background-color: {theme_settings['secondary_color']} !important;
    color: {theme_settings['dark_font']} !important;
    border-radius: 10px !important;  /* Adjust radius as needed */
    border: 2px solid {theme_settings['primary_color']} !important;
}}

.slower:hover, .first:hover, .previous:hover, .reverse:hover, .pause:hover, .play:hover, .next:hover, .last:hover, .faster:hover {{
    background-color: {theme_settings['secondary_ll_color']} !important;
    color: {theme_settings['dark_font']} !important;
    border-radius: 10px !important;  /* Adjust radius as needed */
    border: 2px solid {theme_settings['primary_color']} !important;
}}

"""

# Define the terminal options for the app
terminal_options = {
    "theme": {
        "background": '#343c43',
        "foreground": theme_settings['secondary_color'],
    },
    "fontSize": 11,
    "fontFamily": "Courier New, monospace"  # Change this to your desired font
}