import QtQuick
import QtQuick.Window
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

GrowingImage {
    source: "qrc:/GamesByGamsby.png"
    maxSizeW: 300/shrinkFactor
    maxSizeH: maxSizeW/2//TODO: Fix this200
    width: maxSizeW
    height: maxSizeH
    fillMode: Image.PreserveAspectCrop
        
    function onClicked() {
        Qt.openUrlExternally("http://linktr.ee/Gamsby")//TODO: translate
    }
}