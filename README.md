
# Pyramid Demo

A demo app using the Pyramid framework.

## Getting Started

1. Clone the project from github with `git clone git@github.com:SalvatoreTosti/pyramid-demo.git`
2. Navigate to the root directory of the project
3. Setup a virtual Python environment by running `python3 -m venv env`
4. Activate the virtual environment with `source env/bin/activate`
5. Run `pip install -r requirements.txt` from the root directory.
6. Run `pip install --upgrade pip setuptools` to ensure setup tools are up to date.
7. (Optional) Run `pip install -e ".[testing]"` to configure project for editing
8. Run the project with `pserve development.ini`

### Prerequisites

* Python 3
* pip

## Using the project

**This section assumes you've followed the _Getting Started_ steps and have the project running**
* Navigate to *http://localhost:6543/invoices* to view the project
The /invoices page allows you create new invoices, create invoice sub-items and view all invoices.
The creation controls are listed at the top of the screen and the invoices are listed afterward.

### Creating Invoices
This control section includes a date input area and a _Create Invoice_ button
* Invoice Date Input
Allows you to specify a date associated with the invoice you create.
* Create Invoice Button
Invoices can be created by clicking the _Create Invoice_ button.

### Creating Invoice Items
This control section includes the following inputs:
* Item Description - Text  
Allows you to specify a description for an Invoice Item.
* Parent ID - Integer  
Allows you to specify the ID of the Invoice to which the Invoice Item will belong.  
**There must be an Invoice in the database with the given ID, non-existent IDs will fail to be created**
* Units - Integer  
Allows you to specify a number of units in the Invoice Item.
* Amount - Decimal (2 digits)  
Allows you to specify a dollar amount in the Invoice Item.

It also includes a _Create Invoice Item_ button.

### Refreshing Invoice View
* The page will automatically update itself to reflect Invoices and Invoice Items added through the UI.
* The page can also be manually updated using the _Refresh Invoices_ button.

### Using the API

#### Response Structure
* **status**  
Numeric digit in 200 or 400 range. Indicate if request was successful.
* **message**  
Human parsable description of errors, only sent on error.
* **payload**  
Relevant response data.

#### Errors by Status Code
* 200 - Request succeeded without error.
* 400 - Request failed because of bad input parameter.

#### /invoice/view
**Description:** Returns a JSON representation of all Invoices and Invoice Items.    
**URL Structure:** `http://localhost:6543/invoice/view`.   
**Example:** `curl -X POST http://localhost:6543/invoice/view`.   
**Parameters:** None.     

#### /invoice/create
**Description:**   
	Creates a new Invoice record.  
	Returns a JSON representation of the created Invoice.  
**URL Structure:** `http://localhost:6543/invoice/create`  
**Example:** `curl -X POST http://localhost:6543/invoice/create`  
**Example:** `curl -d "{\"date\":\"0\"}" -X POST http://localhost:6543/invoice/create`  
**Parameters:** `{"date": "10000"}`  
* _date_ - Integer, must be positive   
Number of seconds  since unix epoch in UTC time.  

####  /item/create
**Description:**   
	Creates a new Invoice Item record.  
	Returns a JSON representation of the created Invoice Item.  
**URL Structure:** `http://localhost:6543/item/create`  
Example: `curl -d "{\"description\":\"example descripton\",\"units\":\"1\",\"amount\":\"1.00\",\"parent_id\":\"1\"}" -X POST http://localhost:6543/item/create  
`
**Parameters:** `{
"description" : "example description",
"units" : "1",
"amount" : "1.00"
"parent_id" : "1"
}`
* _description_ - String.  
Text description for Inventory Item.  
* _units_ - Integer, must be positive.  
* _amount_ - Float, must be positive.  
Represents a dollar amount, floats with precision over 2 decimal places will be rounded to 2 decimal places.  
* _parent_id_ - Integer, must be positive.  
ID of an Inventory record in the database.  
Non-existent IDs will return an error.  

## Running the tests

Tests can be run with the `pytest` command.
This command should be run from the root directory of the project.

## Built With

* [pyramid](https://trypyramid.com/) - The web framework used

## Authors

* **Salvatore Tosti** - *Initial work* - [SalvatoreTosti](https://github.com/SalvatoreTosti)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
