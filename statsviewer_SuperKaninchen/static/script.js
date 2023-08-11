const submitSettingsForm = () => {
    document.forms["settings-form"].submit()
}

const timeframe_select = document.getElementById("timeframe-select")
timeframe_select.addEventListener("change", submitSettingsForm)

const view_select = document.getElementById("view-select")
view_select.addEventListener("change", submitSettingsForm)