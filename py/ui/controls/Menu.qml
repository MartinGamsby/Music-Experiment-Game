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
        text: tr("DROPS_OF_WATER")
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
        text: tr("SELECT_MIDI_FILE")
        onClicked: {
            fileDialog.open()
        }
    }
    
    FileDialog {
        id: fileDialog
        currentFolder: backend ? backend.get_media_folder() : ""
        nameFilters: [tr("MIDI_FILES_FILTER")]
        onAccepted: {
            backend.ok_pressed(selectedFile)
        }
    }
    
    CheckBox {
        id: cbGenerate
        text: tr("SETTING_GENERATE_MP3")
        checked: model ? model.p_generate_mp3 : false
        onClicked: {
            model.set_generate_mp3(checked)
        }
    }
    Item {
        Layout.fillHeight: true
    }
    
    GameLogo {
    }
}
