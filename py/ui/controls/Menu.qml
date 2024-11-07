import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Basic
import QtQuick.Controls.Material
import QtQuick.Dialogs

// For State and MusicState enums
import com.martingamsby.music 1.0

ColumnLayout {
    id: menuRoot
    readonly property color backgroundColor: "#222222"
    component MusicButton: Button {        
        implicitWidth: 150
        Layout.rightMargin: 10
        enabled: model ? model.p_music_state_id != MusicStateEnum.GENERATING : false // TODO: Not enough ... ?
    }
	
    
    MusicButton {
        text: "Drops of water"
        onClicked: {
            backend.ok_pressed("")
        }
    }
    MusicButton {
        text: "town"
        onClicked: {
            backend.ok_pressed("assets/town.mid")
        }
    }
    MusicButton {
        text: "flourish"
        onClicked: {
            backend.ok_pressed("assets/flourish.mid")
        }
    }
    MusicButton {
        text: "onestop"
        onClicked: {
            backend.ok_pressed("assets/onestop.mid")
        }
    }
    MusicButton {
        text: "1812 Overture"
        onClicked: {
            backend.ok_pressed("assets/1812 Overture.mid")
        }
    }
    MusicButton {
        text: "Select MIDI file ..."
        onClicked: {
            fileDialog.open()
        }
    }
    
    FileDialog {
        id: fileDialog
        currentFolder: backend ? backend.get_media_folder() : ""
        nameFilters: ["MIDI files (*.mid)"]
        onAccepted: {
            backend.ok_pressed(selectedFile)
        }
    }
    
    CheckBox {
        id: cbGenerate
        text: "Generate Beautiful\nMidi files\n(Slower, might lag)"
        checked: model ? model.p_generate_mp3 : false
        onClicked: {
            model.set_generate_mp3(checked)
        }
    }
    Item {
        Layout.fillHeight: true
    }
    Image {
        id: image
        Layout.maximumWidth: 100
        Layout.maximumHeight: 100
        Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
        source: "qrc:/logo"
        fillMode: Image.PreserveAspectFit
        mipmap: true
        smooth: true
    }
}
