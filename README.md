# Flask-sales-UI

Templates under this repository creates sales table that records sales-relevant informations like:
  `order_id`,
  `quantity`,
  `unitprice`,
  `status`,
  `orderdate`,
  `product category`,
  `sales manager`,
  `shipping cost`,
  `delivery time`,
  `shipping address`,
  `product code`,
  `last updated time`
  
The records get stored in MySQL database(post=3306); users must provide credentials to their MySQL database server by editing `config.json` file

Repository structure:

`sample data`: data values to test run the template with
`static`: contains static files that don't require constant modifications like `config.json` and `main.css`
`template`: html files for table UI

Type <font color=skyblue>python3 app.py</font> to start up the Flask UI in your localhost(port=5000 by default)
