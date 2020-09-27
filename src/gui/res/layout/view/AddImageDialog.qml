import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    width: parent.width * Consts.DialogWidthCoefficient
    anchors.centerIn: Overlay.overlay
    title: Consts.AddImgButtonText
    modal: true
    closePolicy: Popup.NoAutoClose
    Overlay.modal: Rectangle { color: Consts.ShadowColor }

    ColumnLayout {
        anchors.fill: parent
        spacing: Consts.SettingsDialogItemSpacing

        Frame {
            Layout.fillWidth: true

            TextField {
                id: addImageDialogNameBox
                objectName: "addImageDialogNameBox"
                width: parent.width
                placeholderText: Consts.AddImageDialogNameTitle
                selectByMouse: true
                onTextChanged: {
                    addImageBtn.enabled = addImageDialogNameBox.text != "" && addImageDialogPathBox.text != ""
                }
            }
        }
        Frame {
            Layout.fillWidth: true

            RowLayout {
                anchors.fill: parent

                TextField {
                    id: addImageDialogPathBox
                    objectName: "addImageDialogPathBox"
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.leftMargin: Consts.AddImageDialogPathBoxLeftMargin
                    Layout.rightMargin: Consts.AddImageDialogPathBoxRightMargin
                    placeholderText: Consts.AddImageDialogImgPathTitle
                    readOnly: true
                    onTextChanged: {
                        addImageBtn.enabled = addImageDialogNameBox.text != "" && addImageDialogPathBox.text != ""
                    }
                }
                Button {
                    objectName: "addImageDialogBrowseBtn"
                    text: Consts.AddImageDialogBrowseBtn
                    highlighted: true
                }
            }
        }
    }
    footer: DialogButtonBox {
        Button {
            id: addImageBtn
            objectName: "addImageBtn"
            enabled: false
            flat: true
            text: Consts.AddImageDialogAddBtn
            DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
        }
        Button {
            flat: true
            text: Consts.DialogCancelButtonText
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            onClicked: {
                addImageDialogNameBox.text = ""
                addImageDialogPathBox.text = ""
            }
        }
    }
}