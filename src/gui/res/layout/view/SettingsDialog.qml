import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15
import QtGraphicalEffects 1.15

Dialog {
    width: parent.width * Consts.DialogWidthCoefficient
    anchors.centerIn: Overlay.overlay
    title: Consts.SettingsButtonText
    modal: true
    closePolicy: Popup.NoAutoClose
    Overlay.modal: Rectangle { color: Consts.ShadowColor }

    ColumnLayout {
        anchors.fill: parent
        spacing: Consts.DialogItemSpacing

        GroupBox {
            Layout.fillWidth: true
            title: Consts.SettingsThemeTitle

            ComboBox {
                id: themeBox
                width: parent.width
                flat: true
                Material.foreground: parent.Material.foreground
                model: Consts.SettingsThemeModels
                currentIndex: settings.theme
            }
        }
        GroupBox {
            Layout.fillWidth: true

            label: RowLayout {
                Label {
                    Layout.leftMargin: 8
                    text: Consts.SettingsGSLevelTitle
                }
                Image {
                    source: Consts.SettingsIconHelpSrc
                    sourceSize.width: Consts.SettingsDialogHelpImageSize
                    sourceSize.height: Consts.SettingsDialogHelpImageSize
                    ToolTip.visible: ma.containsMouse
                    ToolTip.delay: Consts.TooltipDelay
                    ToolTip.text: Consts.SettingsGSLevelTooltip

                    MouseArea {
                        id: ma
                        anchors.fill: parent
                        hoverEnabled: true
                    }
                    ColorOverlay {
                        anchors.fill: parent
                        source: parent
                        color: window.Material.foreground
                    }
                }
            }
            TextField {
                id: grayscaleBox
                width: parent.width
                text: settings.grayscale
                placeholderText: "Enter something here..."  // TODO
                selectByMouse: true
            }
        }
    }
    footer: DialogButtonBox {
        Button {
            flat: true
            text: Consts.SettingsDialogSaveButtonText
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            onClicked: {
                settings.theme = themeBox.currentIndex
                settings.grayscale = grayscaleBox.text
            }
        }
        Button {
            flat: true
            text: Consts.DialogCancelButtonText
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            onClicked: {
                themeBox.currentIndex = settings.theme
                grayscaleBox.text = settings.grayscale
            }
        }
    }
}