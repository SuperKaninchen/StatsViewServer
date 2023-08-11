const settings_form = document.forms["settings-form"]
const submitSettingsForm = () => {
    settings_form.submit()
}
const toggleSettingsForm = (heading) => {
    if (settings_form.style.display == "none") {
        settings_form.style.display = "block";
        heading.innerHTML = "Settings (hide)"
    } else {
        settings_form.style.display = "none";
        heading.innerHTML = "Settings (show)"
    }
    settings_form.style.visibility = !settings_form.style.visibility
    console.log("toggling")
}

const timeframe_select = document.getElementById("timeframe-select")
timeframe_select.addEventListener("change", submitSettingsForm)

const view_select = document.getElementById("view-select")
view_select.addEventListener("change", submitSettingsForm)

const settings_heading = document.getElementById("settings-heading")
settings_heading.addEventListener("click", function () {toggleSettingsForm(settings_heading)})