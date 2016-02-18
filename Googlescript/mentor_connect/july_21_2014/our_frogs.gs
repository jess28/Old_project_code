function doGet() {
  var html = HtmlService.createTemplateFromFile('index2').evaluate().setTitle('Web App')
       .setSandboxMode(HtmlService.SandboxMode.NATIVE);
  return html;
}
