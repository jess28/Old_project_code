function doGet() {
  var html = HtmlService.createTemplateFromFile('index').evaluate().setTitle('Error')
     .setSandboxMode(HtmlService.SandboxMode.NATIVE);
  return html;
}
