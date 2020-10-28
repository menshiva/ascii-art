import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15
import Qt.labs.settings 1.0
import "view"

ApplicationWindow {
    id: window
    Material.theme: Material[Consts.SettingsThemeModels[settings.theme]]
    Material.primary: Material.Teal
    Material.accent: Material.Teal
    minimumWidth: Consts.ApplicationMinWidth
    minimumHeight: Consts.ApplicationMinHeight
    title: Consts.ProjectName
    visible: true

    Settings {
        id: settings
        objectName: "settings"
        property alias width: window.width
        property alias height: window.height
        property int theme: 0
        property string grayscale: ""
        property double animationDuration: Consts.DefaultAnimationDuration
    }
    FontLoader {
        id: modenineFont
        source: Consts.FontSrc
    }

    ColumnLayout {
        anchors.fill: parent

        MainToolbar { Layout.fillWidth: true }
        GroupBox {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.margins: Consts.ArtLayoutMargins

            TextEdit {
                id: artLayout
                objectName: "artLayout"
                anchors.fill: parent
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.family: modenineFont.name
                font.pixelSize: Consts.DefaultArtSize
                font.kerning: false
                font.preferShaping: false
                textFormat: Text.PlainText
                clip: true
                readOnly: true
                selectByMouse: true
                selectionColor: Material.primary
                color: Material.foreground
            }
        }
    }

    SideDrawer { id: drawer }
    ImageDialog { objectName: "imageDialog" }
    SettingsDialog { id: settingsDialog }
}