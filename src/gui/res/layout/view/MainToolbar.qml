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
            Layout.fillWidth: true
            leftPadding: Consts.ToolbarTitlePadding
            text: Consts.ToolbarTitle
            font.pixelSize: Consts.ToolbarTitleFontSize
        }
        Slider {
            id: artSizeSlider
            Material.accent: Consts.SliderColor
            snapMode: Slider.SnapAlways
            from: 1
            stepSize: 1
            to: 25
            value: Consts.DefaultArtSize
            onMoved: Gui.change_art_size(value)

            ToolTip {
                parent: artSizeSlider.handle
                visible: artSizeSlider.hovered && !artSizeSlider.pressed
                text: Consts.SliderTooltip
            }
            ToolTip {
                parent: artSizeSlider.handle
                visible: artSizeSlider.pressed
                text: artSizeSlider.value
            }
        }
        ToolSeparator {}
        ToolButton {
            id: playAnimBtn
            objectName: "playAnimBtn"
            enabled: false
            icon.source: Consts.PlayButtonImgSrc
            text: Consts.PlayButtonText
            onClicked: {
                enabled = false
                artSizeSlider.enabled = false
                stopAnimBtn.enabled = true
            }
        }
        ToolButton {
            id: stopAnimBtn
            objectName: "stopAnimBtn"
            enabled: false
            icon.source: Consts.StopButtonImgSrc
            text: Consts.StopButtonText
            onClicked: {
                enabled = false
                artSizeSlider.enabled = true
                playAnimBtn.enabled = true
            }
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