/// <reference path="../pb_data/types.d.ts" />
onRecordAfterCreateSuccess((e) => {
  const message = new MailerMessage({
    from: {
      address: $app.settings().meta.senderAddress,
      name: $app.settings().meta.senderName
    },
    to: [{ address: "authx.innovators@example.com" }],
    subject: "New Contact Form Submission",
    html: "<h2>New Contact Submission</h2><p><strong>Name:</strong> " + e.record.get("name") + "</p><p><strong>Email:</strong> " + e.record.get("email") + "</p><p><strong>Message:</strong><br>" + e.record.get("message") + "</p>"
  });
  $app.newMailClient().send(message);
  e.next();
}, "contacts");