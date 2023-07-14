import fitz
import re

def extract_integer(string):
    integer_list = re.findall(r'\d+', string.replace(',', ''))
    if len(integer_list) == 1:
        return int(integer_list[0])
    elif len(integer_list) > 1:
        return [int(x) for x in integer_list]
    else:
        return None

def generate_blocks(input_list):
    sorted_list = sorted(input_list, key=lambda x: x['bbox'][0])
    current_block = {'text': sorted_list[0]['text'], 'bbox': sorted_list[0]['bbox']}
    result_list = [current_block]
    for item in sorted_list[1:]:
        x0 = item['bbox'][0]
        x1 = item['bbox'][2]

        current_x0 = current_block['bbox'][0]
        current_x1 = current_block['bbox'][2]
        
        distance = x0 - current_x1
        
        if distance <= 3 or current_x1 >= x0:
            current_block['text'] += ' ' + item['text']
            
            current_block['bbox'] = (current_x0, min(current_block['bbox'][1], item['bbox'][1]),
                                     x1, max(current_block['bbox'][3], item['bbox'][3]))
        else:
            current_block = {'text': item['text'], 'bbox': item['bbox']}
            result_list.append(current_block)
    
    return result_list

def process_2d_list(input_list):
    result_list = []

    for element in input_list:

     
        if len(element) > 2:
            processed_element = []
            string_data = ""
            for i in element:
                if i == "\t" or i == "�":
                    processed_element.append("0")
                if i.isdigit():
                    processed_element.append(i)
                else:
                    string_data += " " + i.replace("\t", " ").replace("�", " ")
            processed_element.append(string_data)
            result_list.append(processed_element)

        else:
            # print(element)
            if element[1] != "\t" or element[1] != '�':
                if element[0].isdigit() and element[1].isdigit():
                    result_list.append([element[1],element[0]])
                elif element[0].isdigit() and isinstance(element[1], (int, float, str)):
                    result_list.append(element)
                elif element[1].isdigit() and isinstance(element[0], (int, float, str)):
                    swap_x = element[1]
                    swap_y = element[0]
                    result_list.append([swap_x, swap_y])
            elif element[1] == "\t" or element[1] == '�':
                # print(element[0])
                # print("+"*70)
                result_list.append(["0",element[0]])

    return result_list

def generate_blocks_with_thresh(input_list, threshold=10, min_x=0):
    sorted_list = sorted(input_list, key=lambda x: x['bbox'][0])

    current_block = {'text': sorted_list[0]['text'], 'bbox': sorted_list[0]['bbox']}
    result_list = [current_block]

    for item in sorted_list[1:]:
        x = item['bbox'][0]

        current_x = current_block['bbox'][0]
        distance = x - (current_x + current_block['bbox'][2])

        if distance <= threshold and current_x >= min_x+10:
            current_block['text'] += ' ' + item['text']

            current_block['bbox'] = (current_x, min(current_block['bbox'][1], item['bbox'][1]),
                                     x + item['bbox'][2], max(current_block['bbox'][3], item['bbox'][3]))
        else:
            current_block = {'text': item['text'], 'bbox': item['bbox']}
            result_list.append(current_block)
    
    return result_list


def group_elements_by_intersection(data):
    groups = [] 
    d_groups = []

    for text, bbox in data:
        group_found = False
        for group in groups:
            for group_text, group_bbox in group:
                if (bbox[0] <= group_bbox[2] and bbox[2] >= group_bbox[0]) or \
                        (group_bbox[0] <= bbox[2] and group_bbox[2] >= bbox[0]):
                    group.append([text, bbox])
                    group_found = True
                    break
            if group_found:
                break

        if not group_found:
            groups.append([[text, bbox]])

    for i in groups:
        temp_list = []
        for j in i:
            temp_list.append(j)
        d_groups.append(temp_list)


    return d_groups



def find_max_x(lst):
    max_value = float('-inf')

    for item in lst:
        if item[2] > max_value:
            max_value = item[2]

    return max_value

def text_blocks_inside_new_blocks(bigger_block, smaller_blocks):

    text_blocks_inside = []
    
    for smaller_block in smaller_blocks:
        smaller_block = smaller_block[0]
        x0, y0, x1, y1 = smaller_block["bbox"]
        
        if x0 > bigger_block[0] and x1 < bigger_block[2] and y0 > bigger_block[1] and y1 < bigger_block[3]:
            text_blocks_inside.append(smaller_block)
    
    return text_blocks_inside



def create_new_block_img(lst,mx):
    new_block = []

    for item in lst:
        x0, y0, x1, y1, lines, block_no, block_type = item
        new_tuple = (x0, y0, mx, y1, lines, block_no, block_type)
        
        if x1-x0 > 60 and y1-y0 > 60:

            # print("trigger", x1-x0, y1-y0)
            new_block.append(new_tuple)
        else:
            pass
    

    return new_block


def filter_strings(strings):
    filtered_list = []
    skip_mode = False

    for string in strings:
        if string.startswith("shipping information") or string.startswith("brand information") or string.startswith("order information"):
            continue

        if string.startswith("billing information"):
            skip_mode = True
            continue

        if skip_mode:
            filtered_list.append(string)
    
    return filtered_list

def create_sublists(strings):
    sublists = []
    sublist = []
    style_indices = [i for i, string in enumerate(strings) if string.startswith("style")]

    for i, string in enumerate(strings):
        if i in style_indices:
            if sublist:
                sublists.append(sublist)
            sublist = [strings[i-1]]
        sublist.append(string)

    if sublist:
        sublists.append(sublist)
    
    return sublists



def remove_last_page(pdf_path):

    doc = fitz.open(pdf_path)
    num_pages = doc.page_count
    
    if num_pages > 0:
        doc.delete_page(num_pages - 1)
        print("Last page removed from the PDF.")
    else:
        print("The PDF is empty and has no pages.")

    output_path = "modified.pdf"
    doc.save(output_path)
    doc.close()
    
    print("Modified PDF saved to", output_path)

def remove_footer(lst):
    l = []

    try: 
        for i in lst:
            
            if i.startswith("order comments"):
                ind = lst.index(i)
                l = lst[:ind]
                break

            else:
                l = lst
    except:
        l = lst
    return l

def generate_color_list(data):
    m_x = 0
    color_list = []
    cx0, cy0, cx1, cy1 = None, None, None, None

    for element in data:
        text = element.get("text").strip().lower().replace("\t", " ")
        bbox = element.get("bbox")

        # print(text)
        # print()
        # print(bbox)

        if text == "colors":
            cx0, cy0, cx1, cy1 = bbox
            m_x = cx1

        else:
            ex0, ey0, ex1, ey1 = bbox
            if cx1 is not None and cy1 is not None and cy1 < ey0 and cx1 <= ex0 <= cx1 + 60.0:
                color_list.append(text)
                m_x = ex1

    return [color_list,m_x]

    

 

def sort_items(item_list):
    sorted_list = sorted(item_list, key=lambda item: (item[1], item[0]))
    return sorted_list

def concat_str(lst,replacable):
    txt = ""
    for i in lst:
        txt += i

    txt.replace(replacable,"")

    return txt



currencies = {
    'United States Dollar': 'usd',
    'Euro': 'eur',
    'Japanese Yen': 'jpy',
    'British Pound': 'gbp',
    'Australian Dollar': 'aud',
    'Canadian Dollar': 'cad',
    'Swiss Franc': 'chf',
    'Chinese Yuan': 'cny',
    'Swedish Krona': 'sek',
    'New Zealand Dollar': 'nzd',
    'Mexican Peso': 'mxn',
    'Singapore Dollar': 'sgd',
    'Hong Kong Dollar': 'hkd',
    'Norwegian Krone': 'nok',
    'South Korean Won': 'krw',
    'Turkish Lira': 'try',
    'Russian Ruble': 'rub',
    'Indian Rupee': 'inr',
    'Brazilian Real': 'brl',
    'South African Rand': 'zar',
    'Danish Krone': 'dkk',
    'Polish Zloty': 'pln',
    'Israeli Shekel': 'ils',
    'Saudi Riyal': 'sar',
    'United Arab Emirates Dirham': 'aed',
    'Czech Koruna': 'czk',
    'Hungarian Forint': 'huf',
    'Colombian Peso': 'cop',
    'Malaysian Ringgit': 'myr',
    'Philippine Peso': 'php',
    'Thai Baht': 'thb',
    'Indonesian Rupiah': 'idr',
    'Icelandic Krona': 'isk',
    'Croatian Kuna': 'hrk',
    'Bulgarian Lev': 'bgn',
    'Romanian Leu': 'ron',
    'Chilean Peso': 'clp',
    'Peruvian Sol': 'pen',
    'Egyptian Pound': 'egp',
    'Vietnamese Dong': 'vnd',
    'Kenyan Shilling': 'kes',
    'Nigerian Naira': 'ngn',
    'Ukrainian Hryvnia': 'uah',
    'Singapore Dollar': 'sgd'
}

def check_initials(strings):
    initials = set(currencies.values())
    result = []
    try:
        for string in strings:
            for initial in initials:
                if initial in string:
                    result.append(initial)
                    break
        if result:
            return result[0]
        else:
            return ""

    except:
        return ""



def annotate_blocks_with_rectangles(pdf_path):

    retrun_list = [] 

    doc = fitz.open(pdf_path)
    full_pdf_data_block = []

    data_for_return = []

    for page in doc:

        blocks = page.get_text_blocks()
        max_x = find_max_x(blocks)


        # print(max_x)
        # print(max_x)


        data_blocks = []
        image_blocks = []

        for x in blocks:
            if x[6] == 0:
                data_blocks.append(x)
            if x[6] == 1:
                image_blocks.append(x)
            else:
                pass
        

        #code to cerate bew section

        new_blocks = create_new_block_img(image_blocks, max_x)
        new_blocks = sort_items(new_blocks)

        dicts = page.get_text("dict")

        
        spans = []

        blocks = dicts["blocks"]
        
        for i in blocks:
            if i["type"] == 0:
                # print(i.keys())
                lines = i["lines"]
                for j in lines:
                    span = j['spans']
                    spans.append(span)
                    
 
        # print(spans)
        text_data_inside_new_block = []
        for new_block in new_blocks:
            tess = text_blocks_inside_new_blocks(new_block, spans)
            text_data_inside_new_block.append(tess)


        size_total = []

        for i in text_data_inside_new_block:
            data_text_size = []
            for j in i:
                if j["text"] == '\t' or j["text"] == ' ' or j["text"].strip() == '' or j["text"] =="�":
                    pass
                else:
                    data_text_size.append({"text":j["text"],"bbox":j["bbox"]})
            size_total.append(data_text_size)


        obj_dicts = []

        
        for i in text_data_inside_new_block:
            
            struct = {} # internal structure of the product


            data = generate_color_list(i)
            max_x_color = data[1]
            colors = data[0]
            colors = [i.replace("�"," ").strip() for i in colors]
            
            # info = generate_blocks_with_thresh(i,max_x_color)  ##secondary optioin 
            info = generate_blocks(i)
            
            info_list = []
            for k in info:
                
                info_list.append(k["text"].lower().split(" "))
                
            for w in info_list:
                if len(w) == w.count("\t") or len(w) == w.count("�"):
                    try:
                        info_list.remove(w)
                    except:
                        pass
            
            info_list = info_list[2:]

            # print(info_list)

            qty_indx = None

            for sub_list in info_list:
                if "qty" in sub_list:
                    for strings_data in sub_list:
                        temp_var = extract_integer(strings_data)
                        if temp_var:
                            qty_indx = info_list.index(sub_list)
                            struct["qty"] = temp_var


            # print(info_list)
            total_price_list = info_list[qty_indx+1:]


            for sub_list in total_price_list:
                cur_data = check_initials(sub_list)
                if "total" in sub_list:
                    for price_info in sub_list:
                        temp_var = extract_integer(price_info)
                        
                        if temp_var:
                            overall = sum(temp_var)
                            struct["total"] = f"{cur_data} {overall}"

            size_info = info_list[:qty_indx]

            temp_size_dict = {}

            ## for processing size data

            # check the length of colors if greate than one then skip it. =======================>here===============
            if len(colors) > 1:

                try:

                    multi_color_item = []
                    for jk in i:

                        if jk["text"] != '�':
                            
                            # print(jk["text"].replace("�", " ") , jk["bbox"] , jk["font"])

                            if (jk["text"].replace("�", " ").lower() == "total" and jk["font"].lower().endswith("bold")) or jk["text"].replace("�", " ").lower() == "colors":
                                pass
                            else:
                                element_total = [jk["text"].replace("�", " ").lower(),jk["bbox"]]
                                # print(element_total)
                                multi_color_item.append(element_total)

                    multi_color_item_block = [op for op in multi_color_item if op[1][0] >= multi_color_item[0][1][0] - 5]
                    unparsed_list = group_elements_by_intersection(multi_color_item_block)
                    parsed_list = []
                    for unparsed_sub in unparsed_list:
                        temp_list_1 = []
                        for unparsed_sub_2 in unparsed_sub:
                            temp_list_1.append(unparsed_sub_2[0])
                        parsed_list.append(temp_list_1)
                    price = []
                    v1 = []
                    k1 = 0
                    for wx in parsed_list:
                        if wx[0] == "qty":
                            struct["qty"] = wx[-1]
                        elif wx[0] == "total":
                            
                            for wx_1 in wx[1:-1]:
                                price.append(wx_1.strip())

                        else:
                            k1 = wx[0]

                            for wx_1 in wx[1:-1]:
                                v1.append(wx_1)
                                

                    struct["total"] = price
                    temp_size_dict[k1] = v1
                    struct["size"] = temp_size_dict

                except:
                    temp_size_dict["nil"] = "!error"
                
               
            else:
                # print(size_info)
                size_info = process_2d_list(size_info)
                # print(size_info)
                # print() 

                for sub_list in size_info:
                    #check wither len of sub_str == integer elements 
                    key_1 = sub_list[1]
                    value_1 = sub_list[0]

                    if key_1 != "�":

                        temp_size_dict[key_1] = value_1
                    else:
                        pass

            struct["size"] = temp_size_dict



            struct["colors"] = colors
            obj_dicts.append(struct)

            for j in i:
                x0, y0, x1, y1 = j["bbox"]
                rect_annot = page.add_rect_annot([x0, y0, x1, y1])
                rect_annot = page.add_rect_annot([x0, y0, x1, y1])
                rect_annot.set_border(width=0.7, dashes=[2]) 
        
        
                
        
        # print(len(new_blocks))
        for block in new_blocks:
            
            x0, y0, x1, y1, lines, block_no, block_type = block
            blue = (0, 0, 1)
            gold = (1,1,0)
            rect_annot = page.add_rect_annot([x0, y0, x1, y1])
            rect_annot.set_border(width=1, dashes=[2]) 
            rect_annot.update(border_color=gold)

        # code to order the blocks in list
        data_blocks = sort_items(data_blocks)
        

        #defining structure

        # --> headers
        text_data = []
        for i in data_blocks:
            txt = i[4].strip()
            txt = txt.replace('\t', ' ')
            txt = txt.replace('\n', ' ')
            txt = txt.lower()
            text_data.append(txt)

        full_pdf_data_block.append(text_data)



        # structure = {

        #     product_name: {
        #         style : "style",
        #         country : "country", **optional
        #         wholesale : "wholeshale",
        #         sugg_retail : "retail",
        #         colors : [color1, colr2],
        #         size_quantity : {
        #             size : "quantity",
        #             size2 : "quantity2",
        #         },
        #         total : "total",
        #         order_info : "order_info",
        #         shipping_info : "shipping",
        #         brand_info : "brand_info",
        #         billing_info : "billing_info",

        #     }
            
        # }
        b_data = text_data
        text_data = []

        for i in b_data:
            data_x = i.replace("�", " ")
            text_data.append(data_x)
        
        header_info = set()
        for i in text_data:
            try:
                if i.startswith("order information") or i.startswith("brand information") or i.startswith("shipping information") or i.startswith("billing information"):
                    header_info.add(i)
            except:
                pass

        footer_info = []
        for i in text_data:
            try:
                if i.startswith("order comments"):
                    
                    ind = text_data.index(i)
                    footer_info = text_data[ind:]
            except:
                pass
        


        
        data_dict = {}

        
        for i in header_info:
            if i and i.startswith("shipping information"):
                data_dict["shipping_information"] = i.replace("shipping information","")
            if i and i.startswith("brand information"):
                data_dict["brand_information"] = i.replace("brand information","")
            if i and i.startswith("order information"):
                data_dict["order_information"] = i.replace("order information","")
            if i and i.startswith("billing information"):
                data_dict["billing_information"] = i.replace("billing information","")
        

        for i in obj_dicts:
            i["shipping_information"] = data_dict["shipping_information"]
            i["brand_information"] = data_dict["brand_information"]
            i["order_information"] = data_dict["order_information"]
            i["billing_information"] = data_dict["billing_information"]

        # print(obj_dicts)

        body_data = filter_strings(text_data)
        body_data = remove_footer(body_data)

        # print(body_data)
        # create sublist for products

        products = create_sublists(body_data)
        products = products[1:]



        # for i in products:
        #     print(i)
        #     print("\n")

        
        #product data dict

        
        indx_1 = 0
        for product in products:
            product_dict = {}

            
            for i in product:

                if i.startswith("style"):
                    product_dict["style"] = i.replace("style", "").strip()
                if i.startswith("wholesale"):
                    x = i
                    i = i.split("  ")
                    i = [item for item in i if item.strip() != ""]

                    wholesale = i[0].split(":")[1]
                    retail = i[1].split(":")[1]

                    # print(wholesale,retail)
                    product_dict["wholesale"] = wholesale
                    product_dict["sugg_retail"] = retail

                    indx = product.index(x)

                    data = product[indx+1:]

            # print(product_dict)
         

            obj_dicts[indx_1]["style"] = product_dict["style"]
            # print(obj_dicts[indx]["style"])
            obj_dicts[indx_1]["wholesale"] = product_dict["wholesale"]
            # print(obj_dicts[indx]["wholesale"])
            obj_dicts[indx_1]["sugg_retail"] = product_dict["sugg_retail"]
            # print(obj_dicts[indx]["sugg_retail"])
            obj_dicts[indx_1]["name"] = product[0]

            indx_1 += 1

        data_for_return.append(obj_dicts)

    
#         for i in obj_dicts:
#             print(
#                 f"""
# name => {i["name"]},
# style => {i["style"]},
# colors => {i["colors"]},
# wholesale => {i["wholesale"]},
# sugg_retail => {i["sugg_retail"]},
# billing_info => {i["billing_information"]},
# order_info => {i["order_information"]},
# shipping_info => {i["shipping_information"]},
# brand_info => {i["brand_information"]}
# size_info => {i["size"]}
# price_info => {i["total"]}
# qty => {i["qty"]}


# =========================================

# """)

        for block in data_blocks:
            x0, y0, x1, y1, lines, block_no, block_type = block
            rect_annot = page.add_rect_annot([x0, y0, x1, y1])
            rect_annot.set_colors(stroke=(1, 0, 0)) 

    output_path = "annotated.pdf"
    doc.save(output_path)
    doc.close()
    
    print("Annotations added and saved to", output_path)
    return data_for_return


# pdf_path = "/home/guatam/Desktop/fiverr/pdf_data_extract/inp_pdf/ORDER_Lauren-Manoogian_2023-10-06_13769226.pdf"
# remove_last_page(pdf_path)
# p = annotate_blocks_with_rectangles("modified.pdf")





