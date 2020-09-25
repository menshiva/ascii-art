import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Material 2.15
import Qt.labs.settings 1.0

ApplicationWindow {
    id: window
    Material.theme: Material[Consts.SettingsThemeModels[settings.theme]]
    Material.primary: Material.Teal
    Material.accent: Material.Teal
    minimumWidth: Consts.ApplicationMinWidth
    minimumHeight: Consts.ApplicationMinHeight
    title: Consts.ToolbarTitle
    visible: true

    Settings {
        id: settings
        property alias width: window.width
        property alias height: window.height
        property int theme: 0
    }

    header: ToolBar {
        Material.foreground: "white"
        leftPadding: Consts.ToolbarPadding
        rightPadding: Consts.ToolbarPadding

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
                enabled: false
                icon.source: Consts.PlayButtonImgSrc
                text: Consts.PlayButtonText
            }
            ToolButton {
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
                    bottomPadding: 0

                    Action {
                        text: Consts.SettingsButtonText
                        onTriggered: {
                            settingsDialog.open()
                        }
                    }
                }
            }
        }
    }
    GroupBox {
        implicitWidth: parent.width
        implicitHeight: parent.height
        anchors.fill: parent
        anchors.margins: Consts.ArtLayoutMargins
        clip: true

        Label {
            objectName: "artLayout"
            anchors.fill: parent
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
    Drawer {
        id: drawer
        width: parent.width * Consts.DrawerWidthCoefficient
        height: parent.height
        Overlay.modal: Rectangle {
            color: Consts.ShadowColor
        }

        ColumnLayout {
            width: parent.width
            height: parent.height
            spacing: 0

            ToolBar {
                Material.foreground: Material.foreground
                Material.background: Material.background
                Layout.fillWidth: true
                leftPadding: Consts.ToolbarPadding
                rightPadding: Consts.ToolbarPadding

                RowLayout {
                    anchors.fill: parent

                    Label {
                        leftPadding: Consts.ToolbarTitlePadding
                        Layout.fillWidth: true
                        text: Consts.DrawerTitle
                        font.pixelSize: Consts.DrawerTitleFontSize
                        font.weight: Font.Bold
                    }
                    ToolButton {
                        objectName: "addImageBtn"
                        icon.source: Consts.AddImgButtonImgSrc
                        ToolTip.visible: hovered
                        ToolTip.delay: Consts.TooltipDelay
                        ToolTip.text: Consts.AddImgButtonTooltip
                        onClicked: drawer.close()
                    }
                }
            }
            ListView {
                id: artList
                objectName: "artList"
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                model: ["kekhguyguyguyguyguyguyguyguguytfytf", "lol"]  // TODO

                delegate: ItemDelegate {
                    width: artList.width
                    height: Consts.ArtListItemHeight
                    leftPadding: Consts.ArtListItemImageWidth + Consts.ArtListItemTextPadding
                    rightPadding: artItemIcon.width + Consts.ArtListItemIconPadding
                    text: modelData
                    font.pixelSize: Consts.ArtListItemTextFontSize
                    highlighted: ListView.isCurrentItem
                    onClicked: {
                        artList.currentIndex = index
                        drawer.close()
                    }

                    Image {
                        width: Consts.ArtListItemImageWidth
                        height: Consts.ArtListItemImageHeight
                        anchors.verticalCenter: parent.verticalCenter
                        source: "../drawable/test.jpg"
                    }
                    RoundButton {
                        id: artItemIcon
                        objectName: "artItemIcon"
                        anchors.rightMargin: Consts.ArtListItemIconPadding
                        flat: true
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        icon.source: Consts.ArtListInfoImgSrc
                        onClicked: drawer.close()
                    }
                }
                ScrollIndicator.vertical: ScrollIndicator { }
            }
        }
    }
    Dialog {
        id: settingsDialog
        width: parent.width * Consts.SettingsDialogWidthCoefficient
        anchors.centerIn: Overlay.overlay
        title: Consts.SettingsDialogTitle
        modal: true
        closePolicy: Popup.NoAutoClose
        Overlay.modal: Rectangle {
            color: Consts.ShadowColor
        }

        ColumnLayout {
            anchors.fill: parent
            spacing: Consts.SettingsDialogItemSpacing

            GroupBox {
                Layout.fillWidth: true
                title: Consts.SettingsThemeTitle
                clip: true

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
                clip: true

                label: RowLayout {
                    Label {
                        Layout.leftMargin: 8
                        text: Consts.SettingsGSLevelTitle
                    }
                    Image {
                        id: helpImg
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
                    }
                }
                TextField {
                    id: grayscaleBox
                    width: parent.width
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
                }
            }
            Button {
                flat: true
                text: Consts.SettingsDialogCancelButtonText
                DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
                onClicked: {
                    themeBox.currentIndex = settings.theme
                    settingsDialog.close()
                }
            }
        }
    }
}