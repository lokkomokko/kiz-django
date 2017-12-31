from main.models import *

data = list(Med.objects.all())
sicks = list(Sicks.objects.all())
underSicks = list(SicksUndergroup.objects.all())
singleSick = list(SicksSingle.objects.all())
adultRange = list(AgeRange.objects.all())
table = []


class TableCreate:
    def __init__(self, ag=None, main_group=True, all_cases=0, all_codes=None,
                 days='null'):
        self.main_group = main_group
        self.all_cases = all_cases
        # self.group = group
        # self.under_group = under_group
        self.all_codes = all_codes
        self.days = days
        self.sex = ''
        self.age_range = {}
        self.ag = ag

        for age in adultRange:
            self.age_range[age.id] = ''

    row = {}

    def create(self, sex):
        if sex == 'муж':
            self.sex = ['man', sex]
        else:
            self.sex = ['girl', sex]

        self.row = {
            # 'group': self.group,
            # 'under_group': self.under_group,
            'sex': self.sex[1],
            'days': self.days,
            'all_cases': self.all_cases,
            'ag': self.ag,
        }

    def get(self):
        return [self.row, self.sex[0]]

    def allCases(self, id, name, sex, array, data=None):
        # print(name, sex)
        days = 0
        count = 0
        ag = {}

        if sex == 'муж':
            sex_name = 'man'
        else:
            sex_name = 'girl'
        for a in array:
            # print(array, '\n\n\n')
            if sex_name in a['data']:
                arr = a['data'][sex_name]
                # print(arr[sex])
                if arr['sex'] == sex:
                    if not a['main_group'] and arr['sex'] == sex and a['name'] == name:
                        # найдено соответствие
                        count = count + arr['all_cases']
                        days = days + arr['days']

                        if len(arr['ag']) > 0:
                            for key, value in arr['ag'].items():
                                try:
                                    ag[key]
                                except KeyError:
                                    ag[key] = value
                                else:
                                    ag[key] = ag[key] + value

        for i in data:
            for s in sicks:
                if s.id == id and i.sex == sex:
                    for single in singleSick:
                        age_count = 0
                        if single.group_name_id == s.id and i.code_id_id == single.id:
                            count = count + 1
                            days = days + i.days
                            adult_range = i.adult_range_id
                            for a in self.age_range:
                                if a == adult_range:
                                    age_count = age_count + 1

                                    try:
                                        ag[a]
                                    except KeyError:
                                        ag[a] = age_count
                                    else:
                                        ag[a] = ag[a] + age_count

        # print(count, days, c)
        # print(ag)
        return [count, days, ag]

    def searchCases(self, u_id, sex, main=None, data=None):
        # так же поиск дней
        days = 0
        count = 0
        age = {}
        type_name = underSicks

        if main:
            type_name = sicks
        for i in data:
            for u in type_name:
                if u.id == u_id and i.sex == sex:
                    for s in singleSick:
                        age_count = 0
                        group_name = s.under_group_name_id
                        if main:
                            group_name = s.group_name_id

                        if group_name == u.id and i.code_id_id == s.id:
                            count = count + 1
                            days = days + i.days
                            adult_range = i.adult_range_id
                            for a in self.age_range:
                                if a == adult_range:
                                    age_count = age_count + 1

                                    try:
                                        age[a]
                                    except KeyError:
                                        age[a] = age_count
                                    else:
                                        age[a] = age[a] + age_count

        return [count, days, age]

    def searchCodes(self, id, main=False, super=False):
        codes = []

        for single in singleSick:
            if super:
                for u in underSicks:

                    if u.group_name_id == id and single.under_group_name_id == u.id:
                        codes.append(single.name)

                if single.group_name_id == id:
                    codes.append(single.name)

                # print(codes)
            else:
                if main:
                    type_name = single.group_name_id
                else:
                    type_name = single.under_group_name_id
                if type_name == id:
                    codes.append(single.name)

        return codes


def findTable(data=data):
    table = []

    counter = 0

    for s in sicks:
        have = False
        # row = TableCreate()
        # print(row.age_range)
        # table[counter]['all_cases'] = 0
        # table[counter]['main_group'] = True

        for under in underSicks:

            if under.group_name_id == s.id:
                # нашли подгруппу

                have = True
                row = TableCreate()

                table.append({})
                table[counter]['id'] = counter
                table[counter]['data'] = {}
                table[counter]['name'] = s.name
                table[counter]['only_sick'] = s.only_sick
                # найдена погруппа
                row.main_group = False

                if not row.all_codes:
                    row.all_codes = row.searchCodes(under.id)
                # print(row.all_codes)
                # print('найдена погруппа')
                # row.searchCodes(under.id)
                for sex in ['муж', 'жен']:
                    case = row.searchCases(under.id, sex, data=data)

                    row.days = case[1]
                    row.all_cases = case[0]
                    # row.group = s.name
                    # row.under_group =under.name
                    row.ag = case[2]
                    row.create(sex)
                    catch_row = row.get()

                    table[counter]['data'][catch_row[1]] = catch_row[0]

                table[counter]['under_group'] = under.name
                table[counter]['main_group'] = row.main_group
                table[counter]['all_codes'] = row.all_codes
                counter = counter + 1

        if have:
            row = TableCreate()
            table.append({})
            table[counter]['name'] = s.name
            table[counter]['id'] = counter
            table[counter]['super'] = True
            table[counter]['data'] = {}
            table[counter]['under_group'] = False
            table[counter]['only_sick'] = s.only_sick
            table[counter]['main_group_codes'] = s.main_group_codes

            if not row.all_codes:
                row.all_codes = row.searchCodes(s.id, True, True)

            for sex in ['муж', 'жен']:
                table[counter]['main_group'] = row.main_group
                table[counter]['all_codes'] = row.all_codes

                case = row.allCases(s.id, s.name, sex, table, data)
                # case = row.searchCases(s.id, sex, True)
                #
                row.ag = case[2]
                row.days = case[1]
                row.all_cases = case[0]
                # row.group = s.name

                row.create(sex)
                catch_row = row.get()
                table[counter]['data'][catch_row[1]] = catch_row[0]

            counter = counter + 1



        else:
            row = TableCreate()
            table.append({})
            table[counter]['name'] = s.name
            table[counter]['id'] = counter
            table[counter]['data'] = {}
            table[counter]['super'] = False
            table[counter]['under_group'] = False
            table[counter]['only_sick'] = s.only_sick
            table[counter]['main_group_codes'] = s.main_group_codes

            if not row.all_codes:
                row.all_codes = row.searchCodes(s.id, True)

            for sex in ['муж', 'жен']:
                case = row.searchCases(s.id, sex, True, data=data)

                row.ag = case[2]
                row.days = case[1]
                row.all_cases = case[0]
                # row.group = s.name
                row.super = True

                row.create(sex)
                catch_row = row.get()
                table[counter]['data'][catch_row[1]] = catch_row[0]

                table[counter]['main_group'] = row.main_group
                table[counter]['all_codes'] = row.all_codes

            counter = counter + 1

    # print(table)

    ready_table = []
    res_array = {}

    for col in table:
        if 'super' in col:
            if col['super']:
                ready_table.append(col)
                for inner_col in table:
                    if not inner_col['main_group'] and inner_col['name'] == col['name']:
                        ready_table.append(inner_col)
            else:
                ready_table.append(col)

    def result(only=False):
        result = {}
        all = {'all_cases': 0, 'days': 0, 'ag': {}}

        for i in ready_table:
            # поиск только болезней

            if only:
                o = i['only_sick']
            else:
                o = True

            if o == True and i['main_group']:
                for k, v in i['data'].items():

                    all['all_cases'] = all['all_cases'] + v['all_cases']
                    all['days'] = all['days'] + v['days']

                    try:
                        result[k]
                    except KeyError:
                        result[k] = {}

                    result[k]['sex'] = v['sex']
                    try:
                        result[k]['days']
                    except KeyError:
                        result[k]['days'] = v['days']

                    else:
                        result[k]['days'] = result[k]['days'] + v['days']
                    try:
                        result[k]['all_cases']
                    except KeyError:
                        result[k]['all_cases'] = v['all_cases']
                    else:
                        result[k]['all_cases'] = result[k]['all_cases'] + v['all_cases']

                    try:
                        result[k]['ag']
                        # all['ag']
                    except KeyError:
                        result[k]['ag'] = {}

                    if len(v['ag']) > 0:
                        for key, value in v['ag'].items():
                            try:
                                # all['ag'][key]
                                result[k]['ag'][key]
                            except KeyError:
                                result[k]['ag'][key] = value
                            else:
                                result[k]['ag'][key] = result[k]['ag'][key] + value

                            try:
                                all['ag'][key]
                            except KeyError:
                                all['ag'][key] = value
                            else:
                                all['ag'][key] = all['ag'][key] + value
                    # print(all['all_cases'])
        return [result, all]

    # res_array = result(res_array)
    # result()
    res = result()

    res_array['only_sick'] = result(True)[0]
    res_array['with_sick'] = res[0]
    res_array['all'] = res[1]

    # print(res_array)
    return [ready_table, res_array]


# findTable()