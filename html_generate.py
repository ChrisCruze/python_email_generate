#import HTML
import HTML
class ButtonLinkCrate(object):
    # D = {'Name':'a','baby':'c'}
    #'baby=c&Name=a'
    def button_link_create(self, D, link_name='meetoo url', url="http://meetoo.site44.com/?"):
        #i = 'EmailName=' + D['EmailName'] + "&" + "TimeSent=" +D['TimeSent']
        i = "&".join([a + "=" + b for a, b in zip(D.keys(), D.values())])
        s = HTML.link(link_name, url + i)
        return s

class HtmlDesign(ButtonLinkCrate):
    def header_color(self, string):
        return "<span style='color:#3b9d97;'><span class='h1' style=''> <font size='4'> %(string)s </font> </span></span>" % { \
            "string": string}

    def header_color_select(self, s, i):
        l = [
            "<span style='color:#3b9d97;'><span class='h1' style=''> <font size='4'> {} </font> </span></span>",
            "<span style='color:#aaaaaa;'><span class='h2' style=''> <font size='3'> {} </font> </span></span>"
        ]
        s = l[i].format(s)
        return s

    def table_wrapper(self, string):

        html = "<table border='0' cellpadding='0' cellspacing='0' bgcolor='#fff'><td align='center' valign='top'> %(string)s </td></table>" % { \
            "string": string}
        return html
        return ''.join(html)

    # Wraps stuff into <table> html tags. Used by email_tables_send.
    def table_body_wrapper(self, string,background_color="F5F5F5"):
        html = "<table border='0' cellpadding='15' cellspacing='0' width='100%%'' bgcolor='#"+background_color+"'><td align='center' valign='top'> %(string)s </td></table>" % {"string": string}
        return html
        return ''.join(html)

    # Wraps string into <p> html tags. Used by email_tables_send.
    def body_wrapper(self, string):
        html = "<p valign='top'> %(string)s </p>" % { \
            "string": string}
        return html
        return ''.join(html)

    def button_create(self, string):
        html = "<div style='vertical-align:top;text-align:center;display:inline-block;font-size:14px;color:#ffffff;border-radius:3px;background-color:orange;margin:20px 0;padding:6px 12px;border:1px solid orange' align='center'><a href='#' style='color:#fff!important;text-decoration:none!important;display:inline-block;background-color:orange;border:0'></a>%(string)s</div>" % { \
            "string": string}
        return html

    def button_create_with_link(self, string, url='google.com'):
        string = HTML.link(string, url)
        html = "<div style='vertical-align:top;text-align:center;display:inline-block;font-size:14px;color:#ffffff;border-radius:3px;background-color:orange;margin:20px 0;padding:6px 12px;border:1px solid orange' align='center'><a href='#' style='color:#fff!important;text-decoration:none!important;display:inline-block;background-color:orange;border:0'></a>%(string)s</div>" % { \
            "string": string}
        # html = "<br>" + string
        html = self.table_body_wrapper(html)
        return html

    # really only suppose to take in one list
    def table_create(self, *args):
        lst = [self.table_body_wrapper(self.table_wrapper(HTML.table( \
            arg[1:], \
            attribs={'style': 'text-align: center'}, \
            header_row=HTML.TableRow(arg[0], bgcolor='D5D4D6'), \
            col_align=['center'] * len(arg[0])
            )) + "") \
               for arg in args]
        lst = ''.join(lst)
        Header = "<table width='100%%' bgcolor='#aaaaaa'><td valign='top' style='margin: 0 20px;padding: 10px 0;'></table>"
        return lst

    def table_section_create(self, name, arg):
        s = self.table_body_wrapper(self.header_color(name) + "" + self.table_wrapper(HTML.table( \
            arg[1:], \
            attribs={'style': 'text-align: center'}, \
            header_row=HTML.TableRow(arg[0], bgcolor='D5D4D6'), \
            col_align=['center'] * len(arg[0])
            )) + "")
        return s

    # this is the items of a tuple
    # e.g. 'table header','table explainer', [['a','b'],['c','d']]
    def table_sections_create(self, *args):

        args = list(args)
        table = args[-1:][0]
        args = args[:-1]

        header_layers_func = lambda l: '<br>'.join([self.header_color_select(s, i) for i, s in enumerate(l)])

        s = self.table_body_wrapper(header_layers_func(args) + "" + self.table_wrapper(HTML.table( \
            table[1:], \
            attribs={'style': 'text-align: center'}, \
            header_row=HTML.TableRow(table[0], bgcolor='D5D4D6'), \
            col_align=['center'] * len(table[0])
            )) + "")
        return s


    #if it's a dictionary then there must be a key called 'input' that would be the input parameter and taken as first
    #argument here.

    #this here is the tuple, or list, or anytning
    # e.g. ('name','a',[['a','b'],['a','c']])
    def html_section_formulate(self, s, input_key='input',background_color ="F5F5F5"):
        if isinstance(s, dict): #if it's a dictionary
            tup = list(s.items())[0]
            print (tup)
            #print tup
            #print tup[1]
            if tup[0] == 'button_create':
                func = HtmlDesign().button_create
            else:
                func = HtmlDesign().button_create
            #func = TextFunctions().func_get_from_classes(tup[0], MandrillEmail)
            if isinstance(tup[1], dict):
                Dict = DictionaryFunctions().key_filter_item_not(tup[1], input_key)
                s = func(tup[1][input_key], **Dict)  #the key name for value would have to be it
            else:
                s = func(tup[1])
        elif isinstance(s, list):
            try:
                s = self.table_create(s)
            except IndexError:#In the case that the list going in is actually suppose to be tuples
                print ("mandrill_api.py, <html_sectino_formulate>")
                s = self.table_sections_create(*s)
        elif isinstance(s, tuple):
            s = self.table_sections_create(*s)
        #s = self.table_section_create(*s)
        else:
            s = self.table_body_wrapper(s,background_color=background_color)
        return s

class EmailHTMLGenerate(HtmlDesign):

    def prettify_html_string(self, s):
        s = str(BeautifulSoup(str(s)))  #MUST TURN INTO STRING HERE OTHERWISE NONETYPE ERROR
        s = s.replace("\n", "").replace("\"", "'")
        return s


    def html_body_formulate(self, *args,**kwargs):
        # if 'background_color' in kwargs.keys() :
        #     l = map(lambda i: self.html_section_formulate(i,background_color=kwargs['background_color']), args)
        #else:
        l = map(self.html_section_formulate, args) #runs a function against each item of the list
        s = ('').join(l)

        Header = "<table width='100%%' bgcolor='#aaaaaa'><td valign='top' style='margin: 0 20px;padding: 10px 0;'></table>"
        if 'table_border' in kwargs.keys() and kwargs['table_border'] == False:
            return s

        s = Header + s + Header
        return s


    def email_body(self, Names, *args):
        """It needs to take in multiple lists and turn it into a series of HTML tables"""
        #attribs={'align': 'center','text-align': 'center','font-family': 'Helvetica','bgcolor': 'blue','colspan':2},\
        #col_align =['center','center','center','center','center'],\
        #'style': 'text-align: center'
        #col_styles = ['background-color:D5D4D6;font-size: large', None, None,None,None]
        lst = [self.table_body_wrapper(self.header_color(name) + "" + self.table_wrapper(HTML.table( \
            arg[1:], \
            attribs={'style': 'text-align: center'}, \
            header_row=HTML.TableRow(arg[0], bgcolor='D5D4D6'), \
            col_align=['center'] * len(arg[0])
            )) + "") \
               for name, arg in zip(Names, args)]
        lst = ''.join(lst)
        Header = "<table width='100%%' bgcolor='#aaaaaa'><td valign='top' style='margin: 0 20px;padding: 10px 0;'></table>"
        lst = Header + lst + Header
        return lst

    def email_body_test(self, *args):
        """It needs to take in multiple lists and turn it into a series of HTML tables"""
        #attribs={'align': 'center','text-align': 'center','font-family': 'Helvetica','bgcolor': 'blue','colspan':2},\
        #col_align =['center','center','center','center','center'],\
        #'style': 'text-align: center'
        #col_styles = ['background-color:D5D4D6;font-size: large', None, None,None,None]
        lst = [self.table_body_wrapper(self.table_wrapper(HTML.table( \
            arg[1:], \
            attribs={'style': 'text-align: center'}, \
            header_row=HTML.TableRow(arg[0], bgcolor='D5D4D6'), \
            col_align=['center'] * len(arg[0])
            )) + "") \
               for arg in args]
        lst = ''.join(lst)
        Header = "<table width='100%%' bgcolor='#aaaaaa'><td valign='top' style='margin: 0 20px;padding: 10px 0;'></table>"
        return lst




def run_example():
    string = 'sample_string'
    lst = [['name', 'value'], ['Chris', '100']]
    tup = ('name', [['name', 'value'], ['Chris', '100']])
    tup2 = ('name', 'next sub', [['name', 'value'], ['Chris', '100']])
    Dict = {'button_create': 'this is my button'}
    Dict2 = {'button_create_with_link': {'input': 'this is my button', 'url': 'yahoo.com'}}

    args = [tup, string, lst, string, string, lst, tup, tup2, Dict, Dict2]
    html = EmailHTMLGenerate().html_body_formulate(*args)
    print (html)

run_example()

