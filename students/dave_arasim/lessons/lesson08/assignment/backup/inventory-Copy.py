#!/usr/bin/env python
'''Mailroom Part 4 for Session 6, Python 210
Written by David K. Arasim - 11/13/18'''

# Imported modules
import platform
import os
from collections import defaultdict

# Global variables
this_os = platform.system()
quit_option = False

#############################################################################################
# Function section

def main():
    global quit_option

    # Build the Donor Dictionary from a text file
    donor_dict = defaultdict(list)
    build_donor_dict(donor_dict)

    # Build the 'thank you' form letter text string
    build_form_text()

    # Build switch_dict with a dict comprehension
    switch_options = [1, 2, 3, 4]
    switch_functions = [send_thank_you, create_report, send_all_thanks, quit_option_true]
    switch_dict = {sw_opt: sw_fun for sw_opt, sw_fun in zip(switch_options, switch_functions)}

    while not quit_option:
        clear_screen()

        print('*'*10,'  Main Menu  ','*'*10)
        print()
        print('1) Send a Thank You to a single donor')
        print('2) Create a Report')
        print('3) Send Thank You letters to all donors')
        print('4) Quit')
        print()
        print('Choose an option: ', end='')

        user_choice = input()
        print()

        try:
            user_choice = int(user_choice)
        except ValueError:
            print('Sorry, but that is not a number')
        else:
            try:
                switch_dict.get(user_choice)(donor_dict)
            except TypeError:
                print('That option: ', user_choice, ' is out of range', sep='')

        print()

        if quit_option:
            print('Quitting process...')
        else:
            print('<cr> to continue... ', end='')
            input()  # input() for pause

    build_donor_text_file(donor_dict)  # Export the Donor Dictionary back to a text file


def clear_screen():
    # Clear the screen based on operating system in use
    global this_os

    if this_os == 'Windows':
        os.system('clear')
    else:
        os.system('cls')


def quit_option_true(donor_dict):
    '''Set the quit_option to true, so function can be selected from switch_dict'''
    global quit_option
    quit_option = True


def build_donor_dict(donor_dict):
    '''Build Donor Dictionary by extracting values from a text file'''
    try:
        with open('donor_dict.txt', 'r') as dictfile:
            while True:
                donor_dict_line = dictfile.readline()
                if not donor_dict_line: break

                donor_dict_name, donor_dict_amts = donor_dict_line.strip().split(':')

                # Build donor_dict with a list comprehension
                donor_dict[donor_dict_name] = [float(amts) for amts in donor_dict_amts.split(',')]

        dictfile.close()
    except FileNotFoundError:
        print()
        print('Donor database in donor_dict.txt not found.  Starting with new, empty database.')
        print()


def build_form_text():
    '''Build the 'thank you' form letter text string'''
    global form_text_str

    form_text = ['Dear {form_name},\n',
                 'Thank you for your generous donation of ${form_amt:.2f}\n',
                 'Please consider this e-mail as record of your donation for tax deduction purposes.\n',
                 'Sincerely, Your Local Charity']
    form_text_str = ''.join(x for x in form_text) # Comprehension
    return form_text_str


def build_donor_text_file(donor_dict):
    '''Export the Donor Dictionary data back to a text file'''
    with open('donor_dict.txt', 'w') as dictfile:
        for this_name, this_amts in donor_dict.items():
            amts_str = ','.join(str(x) for x in this_amts) # Comprehension
            this_line = this_name + ':' + amts_str + '\n'

            dictfile.write(this_line)

    dictfile.close()


def send_thank_you(donor_dict):
    '''Sends thank you letter to single donor as their donation is made and recorded'''
    quit_thank_you = False

    clear_screen()

    while not quit_thank_you:
        print("Enter Donor's name, type 'list' for existing Donors (<cr> to exit): ", end='')

        donor_choice = input()
        print()

        if donor_choice == '': quit_thank_you = True
        elif donor_choice == 'list': print(show_donor_list(donor_dict))
        else:
            donation_amt = find_donor(donor_dict, donor_choice)
            thank_donor(donor_choice, donation_amt)
            quit_thank_you = True


def show_donor_list(donor_dict):
    '''Show the Donor List of names only'''
    donor_list = 'List of Donors'
    donor_list_w = 26

    # Donor list header
    list_nom = (donor_list, donor_list_w)
    list_out = '{:{}}\n'.format(*list_nom)
    list_out += '-'*donor_list_w + '\n'

    # Donor list body
    for this_name in donor_dict:
        # Data line
        this_line = (this_name, donor_list_w)
        list_out += '{:{}}\n'.format(*this_line)

    list_out += '\n'

    return list_out


def find_donor(donor_dict, donor_choice, donation_amt = None):
    '''Finds an existing Donor OR installs a new Donor and records donation amount'''
    valid_amt = False

    while not valid_amt:
        if donation_amt is None:
            print('Please enter donation amount for ', donor_choice, ': $', sep='', end='')
            donation_amt = input()

        try:
            donation_amt = float(donation_amt)
        except ValueError:
            print('Sorry but that is not a valid amount')
            print()
        else:
            valid_amt = True

    donor_dict[donor_choice].append(donation_amt)

    return donation_amt


def thank_donor(donor_choice, donation_amt):
    '''Send a thank you letter to current Donor for current donation only'''
    print()
    print('E-mail form letter output:')
    print()
    print(build_form_text_out(donor_choice, donation_amt))
    print()
    print('End e-mail form letter output, <cr> to continue... ', end='')
    input()  # input() for pause


def build_form_text_out(form_name, form_amt):
    '''Builds form text output from form_text_str and its related format values'''
    global form_text_str

    form_dict = {'form_name': form_name, 'form_amt': form_amt}
    return form_text_str.format(**form_dict)


def send_all_thanks(donor_dict):
    '''Send thank you letters to all donors as text files named as donor_name.txt'''
    for this_name, this_amts in donor_dict.items():
        this_tot = sum(this_amts)
        this_file = this_name.replace(' ', '_') + '.txt'

        with open(this_file, 'w') as thank_you_file:
            thank_you_file.write(build_form_text_out(this_name, this_tot))

        thank_you_file.close()

        print('Created Thank You letter: ', this_file)


def create_report(donor_dict, report_rtn = None):
    '''Report of Donors with donation summary: Total Given|Number of Gifts|Average Gift Amount'''
    donor_name = 'Donor Name'
    tot_given = 'Total Given'
    num_gifts = 'Num Gifts'
    avg_gift = 'Average Gift'
    sep_char = '|'

    donor_name_w = 26
    tot_given_w = 13
    num_gifts_w = 11
    avg_gift_w = 13
    sep_char_w = len(sep_char)

    # Report header
    header_nom = donor_name, donor_name_w, sep_char, tot_given, tot_given_w, sep_char
    header_nom += num_gifts, num_gifts_w, sep_char, avg_gift, avg_gift_w
    report_out = '{:{}}{}{:>{}}{}{:>{}}{}{:>{}}\n'.format(*header_nom)
    report_out += '-'*donor_name_w + '-'*sep_char_w + '-'*tot_given_w + '-'*sep_char_w
    report_out += '-'*num_gifts_w + '-'*sep_char_w + '-'*avg_gift_w + '\n'

    # Report body
    for this_name, this_amts in donor_dict.items():
        this_tot = sum(this_amts)
        this_cnt = len(this_amts)

        # Avoid division by zero
        if this_cnt != 0:
            this_avg = this_tot / this_cnt
        else:
            this_avg = 0

        # Data line
        this_line = this_name, donor_name_w, this_tot, (tot_given_w - 1)
        this_line += this_cnt, num_gifts_w, this_avg, (avg_gift_w - 1)
        report_out += '{:{}} ${:{}.2f} {:{}} ${:{}.2f}\n'.format(*this_line)

    if report_rtn is None:
        print(report_out)
    else:
        return report_out

#############################################################################################
# Main section

if __name__ == "__main__":
    # Guards against code running automatically if this module is imported
    main()
