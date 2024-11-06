import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material


Image {
    fillMode: Image.PreserveAspectCrop
    width: 300
    height: width/2
    source: "qrc:/GamesByGamsby.png"
    MouseArea {
        anchors.fill: parent
        onClicked: {
            Qt.openUrlExternally("http://linktr.ee/Gamsby")
        }
    }
}