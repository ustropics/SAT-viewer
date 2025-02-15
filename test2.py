import panel as pn

# Initialize Panel's extension
pn.extension()

# Define the dropdown widgets
dropdown1 = pn.widgets.Select(name='Dropdown 1', options=['Option A', 'Option B', 'Option C'])
dropdown2 = pn.widgets.Select(name='Dropdown 2', options=['Option 1', 'Option 2', 'Option 3'])

# Main frame (a container pane that supports dynamic updates)
main_frame = pn.Column("**Initial Content**")

# Define a function to update the main frame with new content
def update_main_frame(*events):
    selected1 = dropdown1.value
    selected2 = dropdown2.value

    # Replace the content of the main frame dynamically
    main_frame.clear()
    main_frame.append(pn.pane.Markdown(f"### Updated Content"))
    main_frame.append(pn.pane.Markdown(f"- Dropdown 1: {selected1}"))
    main_frame.append(pn.pane.Markdown(f"- Dropdown 2: {selected2}"))

# Attach the update function to both dropdowns
dropdown1.param.watch(update_main_frame, 'value')
dropdown2.param.watch(update_main_frame, 'value')

# Layout with a sidebar and main frame
layout = pn.Row(
    pn.Column(dropdown1, dropdown2, width=200, sizing_mode="fixed"),  # Sidebar
    pn.Spacer(width=20),  # Optional spacing
    main_frame,  # Main frame
)

# Serve the application
layout.servable()
