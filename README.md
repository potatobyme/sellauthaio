# Developer:
- garvwasthere





# Sellauth AIO
A full working AIO source code that lets you access your Sellauth via Discord bot.

## List of Commands:
![image](https://cdn.discordapp.com/attachments/1305835611403325482/1331320370816614522/image.png?ex=67913037&is=678fdeb7&hm=5da290647462957a67842e7b8ab96c2719cc7c693eddd7135ce074fbecc1bf95&)

## Command Details:

### Balance Command
- **Usage**: `.bal`
- **Description**: Shows the current balance of your Sellauth account.

### Payout Command
- **Usage**: `.payout {LitecoinAddress} {Amount}`
- **Description**: Withdraws balance from Sellauth to specified LTC address.
- **Example**: `.payout LTC123456789 15`
- **Note**: Don't add $ sign, just use the number.

### GetStock Command
- **Usage**: `.getstock {ProductID}`
- **Description**: DMs you all stock of the specified product.
- **Example**: `.getstock 123`

### Invoice Command
- **Usage**: `.invoice {InvoiceID}`
- **Description**: DMs you detailed information about the specified invoice.
- **Example**: `.invoice ABC123-456`

### Payment Command
- **Usage**: `.payment {Amount}`
- **Description**: Creates a payment invoice with QR code.
- **Example**: `.payment 25`

### Process Command
- **Usage**: `.process {OrderID}`
- **Description**: Manually processes an order without payment.
- **Example**: `.process XYZ789`

### Restock Command
- **Usage**: `.restock {ProductID}`
- **Description**: Restocks product directly from Discord without accessing Sellauth.
- **Example**: `.restock 456`

### Stock Command
- **Usage**: `.stock`
- **Description**: Shows current stock levels of all products.

### Replace Command
- **Usage**: `.replace {OrderID} {Range}`
- **Description**: Replaces defective products in an order.
- **Example**: `.replace 345432 0-50`
- **Note**: Range starts from 0 (e.g., 0-50 replaces first 51 items)

### Calc Command
- **Usage**: `.calc {Number1} {Operation} {Number2}`
- **Description**: Performs basic mathematical calculations.
- **Example**: `.calc 10 * 5`

### CheckCPN Command
- **Usage**: `.checkcpn`
- **Description**: Shows list of available usable coupons.

### RestockNotif Command
- **Usage**: `.restocknotif`
- **Description**: Sends restock notification to the designated restock channel.

### CouponCreate Command
- **Usage**: `.couponcreate {DiscountPercentage} {CouponName} {ProductID}`
- **Description**: Creates a new discount coupon.
- **Example**: `.couponcreate 15 SUMMER123 789`

### CouponDelete Command
- **Usage**: `.coupondelete {CouponID}`
- **Description**: Deletes an existing coupon.
- **Example**: `.coupondelete ABC123`

### CouponEdit Command
- **Usage**: `.couponedit {CouponID} {NewCode} {ProductID} {NewDiscountAmount}`
- **Description**: Edits an existing coupon's details.
- **Example**: `.couponedit ABC123 WINTER50 789 50`

### Update Command
- **Usage**: `.update {ProductID} {NewPrice}`
- **Description**: Updates product price and information.
- **Example**: `.update 123 29.99`

  ### Purchase Command
- **Usage**: `.purchase {COUPON} {email} {amount}`
- **Description**: Purchases product directly via discord instead of sellauth.
- **Example**: `.purchase couponxyz xyz@xyz.com 2000`

  ### GetDelivery Command
- **Usage**: `.getdelivery {invoice_id}`
- **Description**: Sends you the product after the payment is done and the confirmations are done.
- **Example**: `.getdelivery xyz-invoiceid`

    ### Stats Command
- **Usage**: `.stats `
- **Description**: Shows statistic of the sellauth.
- **Example**: `.stats`
  
## Permission Levels
- Some commands require specific permission levels (Owner, Admin, Staff)
- Make sure to configure permissions in config.json

## Setup
1. Configure your config.json with required tokens and IDs
2. Set up webhook URLs for logging
3. Configure permission levels for different commands

## Note
- Keep your config.json secure and never share it
- Some commands send responses via DM for security
- All amounts should be entered without currency symbols

