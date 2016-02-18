function doGet() {
  var html = HtmlService.createTemplateFromFile('index').evaluate().setTitle('About')
     .setSandboxMode(HtmlService.SandboxMode.NATIVE);
  return html; 
}