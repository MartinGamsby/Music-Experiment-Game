import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material


Image {
    id: image
    Layout.maximumWidth: 100
    Layout.maximumHeight: 100
    Layout.alignment: Qt.AlignRight | Qt.AlignBottom
    source: "qrc:/logo"
    fillMode: Image.PreserveAspectFit
    mipmap: true
    smooth: true
    
    MouseArea {
        anchors.fill: parent
        onClicked: {
            backend.toMainMenu(true)
        }
    }
}