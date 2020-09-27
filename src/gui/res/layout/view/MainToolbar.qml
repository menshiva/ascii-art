import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15

ToolBar {
    Material.foreground: "white"
    leftPadding: Consts.ToolbarPadding
    rightPadding: leftPadding

    RowLayout {
        anchors.fill: parent

        ToolButton {
            icon.source: Consts.DrawerButtonImgSrc
            onClicked: drawer.open()
        }
        Label {
            leftPadding: Consts.ToolbarTitlePadding
            Layout.fillWidth: true
            text: Consts.ToolbarTitle
            font.pixelSize: Consts.ToolbarTitleFontSize
        }
        ToolButton {
            //objectName: "playAnimBtn"  TODO
            enabled: false
            icon.source: Consts.PlayButtonImgSrc
            text: Consts.PlayButtonText
        }
        ToolButton {
            //objectName: "stopAnimBtn"  TODO
            enabled: false
            icon.source: Consts.StopButtonImgSrc
            text: Consts.StopButtonText
        }
        ToolSeparator {}
        ToolButton {
            icon.source: Consts.MoreButtonImgSrc
            onClicked: settingsMenu.open()

            Menu {
                id: settingsMenu
                y: parent.height
                topPadding: 0
                bottomPadding: topPadding

                Action {
                    text: Consts.SettingsButtonText
                    onTriggered: settingsDialog.open()
                }
            }
        }
    }
}