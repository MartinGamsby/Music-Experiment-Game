import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

ColumnLayout {
    FlagButton {
        text: "English" // Don't translate, use language's own wording
        hl: "en"
    }
    FlagButton {
        text: "Français" // Don't translate, use language's own wording
        hl: "fr"
    }
}