function doGet() {
  var html= HtmlService.createTemplateFromFile('index').evaluate().setTitle('Results')
       .setSandboxMode(HtmlService.SandboxMode.NATIVE);
  return html;
}
