function doGet() {
  var html = HtmlService.createTemplateFromFile('index').evaluate().setTitle('Frogs and Human Health')
       .setSandboxMode(HtmlService.SandboxMode.NATIVE);
  return html;
}