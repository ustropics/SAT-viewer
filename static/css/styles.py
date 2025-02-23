# Define the default theme settings for the app
theme_settings = {
    'primary_color': '#782f40',
    'secondary_color': '#CEB888',

    'primary_hl_color': '#b80b0e',
    'secondary_hl_color': '#FFD700',

    'primary_bg_color': '#212529',
    'secondary_bg_color': '#343c43',
    'success_bg_color': '#428a4d',
    'warning_bg_color': '#8a4242',

    'primary_low_color': '#3b121c',
    'secondary_low_color': '#54421c',

    'light_font': '#f8f9fa',
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

#operations-usage ~ p{{
    color: {theme_settings['dark_font']} !important;
}}

select option:focus, 
select option:active, 
select option:checked
{{
    background: linear-gradient({theme_settings['secondary_color']},{theme_settings['secondary_color']});
    background-color: {theme_settings['secondary_color']} !important;
    color: {theme_settings['dark_font']} !important;
    text-shadow: none !important;
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


.xterm-helpers {{}}

.bk-panel-models-markup-HTML {{
    width: 1500px !important!;
    max_width: 1500px !important;
}}


.main-content {{
    background-color: {theme_settings['secondary_bg_color']} !important;
}}

.mdc-top-app-bar {{
    background-color: {theme_settings['primary_color']} !important;
}}

.bk-btn-primary {{
    background-color: {theme_settings['secondary_color']} !important;
    color: {theme_settings['dark_font']} !important;
    border: none;
    cursor: pointer;
}}

.bk-btn-primary:hover {{
    background-color: {theme_settings['secondary_hl_color']} !important;
    color: {theme_settings['dark_font']} !important;
    border: none;
    cursor: pointer;
}}

.bk-btn-success {{
    background-color: {theme_settings['primary_color']} !important;
    color: {theme_settings['light_font']} !important;
    border: none;
    cursor: pointer;
}}

.bk-btn-success:hover {{
    background-color: {theme_settings['primary_hl_color']} !important;
    color: {theme_settings['light_font']} !important;
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
    max-width: 330px;
    box-sizing: border-box;
    scrollbar-color: {theme_settings['secondary_color']} {theme_settings['primary_color']};
    }}
"""

# Define the terminal options for the app
terminal_options = {
    "theme": {
        "background": '#343c43',
        "foreground": '#FFD700',
    },
    "fontSize": 11
}