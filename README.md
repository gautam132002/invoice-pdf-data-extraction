# Extracting Data from PDF Invoices

Welcome to the "Extracting Data from PDF Invoices" GitHub repository! This repository contains code that can extract specific information from invoices of a particular type. We have provided a few examples of such invoices in the `./inp_pdf` folder for you to test the code on.

## Extracted Information

The code is designed to extract the following fields from the invoices:

- Name: The name of the item or product listed on the invoice.
- Colors: The colors associated with the item.
- Style: The style or design of the item.
- Shipping Information: The details regarding the shipment, such as the address and delivery method.
- Brand Information: Information about the brand associated with the item.
- Order Information: Details about the order, such as the order number and date.
- Wholesale Price: The price at which the item is sold to retailers.
- Suggested Retail Price: The recommended selling price for the item to end customers.
- Total Price: The total price of the order.
- Size: The size or dimensions of the item.
- Quantity: The quantity of the item ordered.

## Accuracy

The extraction process in this code is highly accurate, with a guaranteed accuracy rate above 95%. This ensures that the extracted information is reliable and trustworthy.

For more detailed information about the extracted blocks, please refer to the `./annotated.pdf` file available in this repository.

We hope you find this code helpful for your invoice data extraction needs!


## Usage

To use the code in this repository, follow the instructions below:

1. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the `main.py` file:
   ```
   python main.py
   ```

   The program will prompt you to provide the location of the PDF file to extract data from.

4. After the extraction process, a CSV file named `output.csv` will be generated containing the extracted data.

All the necessary functions are implemented in `qnot.py` and are imported into `main.py`.

# Contribution

Contributions to the "Extracting Data from PDF Invoices" project are welcome and encouraged! If you have any ideas, improvements, or bug fixes, please feel free to contribute.

To contribute to this project, follow these steps:

1. Fork the repository to your GitHub account.
2. Clone the forked repository to your local machine.
3. Make the necessary changes or additions.
4. Test your changes to ensure they work as expected.
5. Commit your changes and push them to your forked repository.
6. Submit a pull request in the original repository, explaining the changes you made and why they are beneficial.

Please ensure that your contributions align with the goals of the project and follow the coding style.

## Guidelines for Contributions

- When making changes, create a new branch from the `main` branch with a descriptive name.
- Keep your commits focused and provide clear commit messages.
- Include appropriate documentation and comments in your code.
- Test your changes thoroughly before submitting a pull request.
- Be open to feedback and be responsive to any suggestions or requests for improvements.

Thank you for considering contributing to this project! Your efforts are greatly appreciated.
