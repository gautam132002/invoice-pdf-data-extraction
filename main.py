import qnot
import csv

def generate_csv(data):
    headers = ["name", "colors", "style", "shipping_information", "brand_information",
               "order_information", "wholesale", "sugg_retail", "total", "size", "quantity"]

    with open("output.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()

        for product in data:
            colors = product["colors"]
            size = product["size"]
            total = product["total"]

            if len(colors) > 1:
                for i in range(len(colors)):
                    for key, value in size.items():
                        row = {
                            "name": product["name"],
                            "colors": colors[i],
                            "style": product["style"],
                            "shipping_information": product["shipping_information"],
                            "brand_information": product["brand_information"],
                            "order_information": product["order_information"],
                            "wholesale": product["wholesale"],
                            "sugg_retail": product["sugg_retail"],
                            "total": total[i],
                            "size": key,
                            "quantity": value[i]
                        }
                        writer.writerow(row)
            else:
                for key, value in size.items():
                    row = {
                        "name": product["name"],
                        "colors": colors[0],
                        "style": product["style"],
                        "shipping_information": product["shipping_information"],
                        "brand_information": product["brand_information"],
                        "order_information": product["order_information"],
                        "wholesale": product["wholesale"],
                        "sugg_retail": product["sugg_retail"],
                        "total": total,
                        "size": key,
                        "quantity": value
                    }
                    writer.writerow(row)
    print("CSV generated sucessfully....")

def get_structure(data, indent=0):
    structure = ""

    if isinstance(data, list):
        structure += "{\n"

        for item in data:
            structure += " " * (indent + 2)
            structure += get_structure(item, indent + 2)

        structure += " " * indent + "}\n"

    elif isinstance(data, dict):
        structure += "{\n"

        for key, value in data.items():
            structure += " " * (indent + 2)
            structure += key + ": "
            structure += get_structure(value, indent + 2)

        structure += " " * indent + "}\n"

    else:
        structure += str(data) + "\n"

    return structure


def collect_size_keys(array):
    size_keys = set()

    for sub_array in array:
        for dictionary in sub_array:
            data_dict = list(dictionary["size"].keys())
            for i in data_dict:
                size_keys.add(i)

    return list(size_keys)


pdf_path = "/home/guatam/Desktop/fiverr/pdf_data_extract/inp_pdf/ORDER_Lauren-Manoogian_2023-10-06_13769226.pdf"

qnot.remove_last_page(pdf_path)
p = qnot.annotate_blocks_with_rectangles("modified.pdf")

temp = []
for i in p:
    for j in i:
        # print()
        # print(j)
        # print("="*50)
        # print()

        temp.append(j)

generate_csv(temp)



x = get_structure(p)




with open("data.json", "w") as f:
    f.write(x)