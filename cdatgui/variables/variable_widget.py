from cdatgui.bases import StaticDockWidget
from PySide import QtCore
from cdatgui.toolbars import AddEditRemoveToolbar
from variable_add import AddDialog
from cdms_var_list import CDMSVariableList
from edit_variable_widget import EditVariableDialog

class VariableWidget(StaticDockWidget):

    selectedVariable = QtCore.Signal(object)

    def __init__(self, parent=None, flags=0):
        super(VariableWidget, self).__init__(u"Variables", parent, flags)
        self.allowed_sides = [QtCore.Qt.DockWidgetArea.LeftDockWidgetArea]

        self.add_dialog = AddDialog(self)
        self.add_dialog.accepted.connect(self.add_variable)

        self.setTitleBarWidget(AddEditRemoveToolbar("Variables",
                                                    self,
                                                    self.add_dialog.show,
                                                    self.edit_variable,
                                                    self.remove_variable))

        self.variable_widget = CDMSVariableList(self)
        self.setWidget(self.variable_widget)

    def select_variable(self, index):
        var = self.variable_widget.get_variable(index)
        self.selectedVariable.emit(var)

    def add_variable(self):
        new_variables = self.add_dialog.selected_variables()
        for var in new_variables:
            self.variable_widget.add_variable(var)

    def load(self, files, vars):
        self.add_dialog.load(files)
        for var in vars:
            self.variable_widget.add_variable(var)

    def edit_variable(self):
        # Edit variable dialog
        indexes = self.variable_widget.selectedIndexes()
        if not indexes:
            return
        index = indexes[0].row()
        variable = self.variable_widget.get_variable(index)
        e = EditVariableDialog(variable, self)
        e.show()

    def remove_variable(self):
        # Confirm removal dialog
        pass  # pragma: nocover
