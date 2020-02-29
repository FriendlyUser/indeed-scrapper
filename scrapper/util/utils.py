def transform(input,sign, quote = False):
    syntax = input.replace(" ", sign)
    if quote == True:
        syntax = ''.join(['"', syntax, '"'])
    return(syntax)

#####################################################
##### Function for Concatenate list data        #####
#####################################################
def concatenate_list_data(list):
    result= ''
    for element in list:
        result += str(element)
    return result

def largest_number(in_str):
    l=[int(x) for x in in_str.split() if x.isdigit()]
    return max(l) if l else None

def get_indeed_url(args):
    BASE_URL_indeed = 'https://ca.indeed.com'
    sign = '+'
    if not args.input_city: # if (input_city is "")
        url_indeed_list = [ BASE_URL_indeed, '/jobs?q=', transform(args.input_job, sign, args.input_quote),
                        '&l=', args.input_state]
        url_indeed = concatenate_list_data(url_indeed_list)
    else: # input_city is not ""
        url_indeed_list = [ BASE_URL_indeed, '/jobs?q=', transform(args.input_job, sign, args.input_quote),
                        '&l=', transform(args.input_city, sign), '%2C+', args.input_state]
        url_indeed = concatenate_list_data(url_indeed_list)
    return url_indeed