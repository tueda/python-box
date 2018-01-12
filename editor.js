var editor = ace.edit("editor");
editor.getSession().setMode("ace/mode/python");
editor.focus();

$(window).on("load", function() {
  brython(1);
});
