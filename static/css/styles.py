css = """
#input {
    background-color: #343c43;
}
.bk-input:active {
    background-color: green;
}

focus {
    background-color: green !important;
    color: inherit; /* Inherit text color from the main select */
}

.bk-input {
    /* Optional customizations for the overall dropdown */
    background-color: transparent;
    border: 1px solid #ccc; /* Customize as needed */
    color: #333; /* Customize text color */
}

/* Remove the blue background when focused */
.bk-input:focus {
    outline: none;
    background-color: transparent;
}

.bk-btn-success {
    background-color: #CEB888 !important;
    color: #2C2A29;
    border: none;
    cursor: pointer;
}

.bk-btn-success:hover {
    background-color: #FFD700 !important;
    color: #2C2A29;
    border: none;
    cursor: pointer;
}

.mdc-top-app-bar {
    background-color: #782F40 !important;
}

.mdc-drawer {
}

.bk-tab.bk-active {
    color: #CEB888 !important;
    outline: none !important;
}

.bk-tab:focus {

  outline: none !important;

}

.main-content {
    background-color: #343c43 !important;
}
"""

terminal_options = {
    "theme": {
        "background": '#141111',
    },
    "font-size": 14
}