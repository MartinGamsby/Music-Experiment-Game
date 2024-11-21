import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material


GrowingImage {
    source: "qrc:/logo"
    maxSize: 100
    function onClicked() {
        backend.toMainMenu(true)
    }
}