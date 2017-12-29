from main.models import *

data = list(Med.objects.all())
sicks = list(Sicks.objects.all())
underSicks = list(SicksUndergroup.objects.all())
singleSick = list(SicksSingle.objects.all())
adultRange = list(AgeRange.objects.all())


class TableCreate:
    def __init__(self, main_group=True, all_cases=0, group='null', under_group=False, all_codes=None, days='null'):
        self.main_group = main_group
        self.all_cases = all_cases
        self.group = group
        self.under_group = under_group
        self.all_codes = all_codes
        self.days = days
        self.sex = ''
        self.age_range = {}
        for age in adultRange:
            self.age_range[age.id] = ''

    row = {}

    def create(self, sex):
        if sex == 'муж':
            self.sex = ['man', sex]
        else:
            self.sex = ['girl', sex]

        self.row = {
            'group': self.group,
            'under_group': self.under_group,
            'sex': self.sex[1],
            'days': self.days,
            'all_cases': self.all_cases,
            'age_range': self.age_range
        }

    # def findRange(self):
    #     for r in self.age_range:
    #         for i in data

    def get(self):
        return [self.row, self.sex[0]]

    def searchCases(self, u_id, sex):
        # так же поиск дней
        days = 0
        count = 0
        age = {}
        for i in data:
            for u in underSicks:
                if u.id == u_id and i.sex == sex:
                    for s in singleSick:
                        age_count = 0

                        if s.under_group_name_id == u.id and i.code_id_id == s.id:
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
                                    # else:
                                    #     age[a] = age_count
                                    # age = [a, age_count]
        # print(age)

        # if i.code_id_id == id and i.sex == sex:
        #     count = count + 1
        #     days = days + i.days

        # print(days)
        return [count, days, age]

    def searchCodes(self, id):
        codes = []
        for single in singleSick:
            if single.under_group_name_id == id:
                codes.append(single.name)
        # print(codes)
        return codes




def findTable():
    table = []

    counter = 0
    counter = 0
    for s in sicks:
        # row = TableCreate()
        # print(row.age_range)
        # table[counter]['all_cases'] = 0
        # table[counter]['main_group'] = True

        for under in underSicks:

            if under.group_name_id == s.id:

                row = TableCreate()

                table.append({})
                table[counter]['id'] = counter

                # найдена погруппа
                row.main_group = False

                if not row.all_codes:
                    row.all_codes = row.searchCodes(under.id)
                # print(row.all_codes)
                # print('найдена погруппа')
                # row.searchCodes(under.id)
                for sex in ['муж', 'жен']:

                    case = row.searchCases(under.id, sex)

                    row.days = case[1]
                    row.all_cases = case[0]
                    row.group = s.name
                    row.under_group = under.name

                    row.create(sex)
                    catch_row = row.get()
                    if case[2]:
                        # print(case[2])
                        for fk, fv in catch_row[0]['age_range'].items():
                            for ck, cv in case[2].items():
                                # print(ck, fk)
                                if ck == fk:
                                    catch_row[0]['age_range'][fk] = cv
                                    # print('yew')
                                    # print(catch_row[0]['age_range'][c])

                    # print(catch_row[0]['age_range'])
                    table[counter][catch_row[1]] = catch_row[0]

                table[counter]['main_group'] = row.main_group
                table[counter]['all_codes'] = row.all_codes
                counter = counter + 1


            else:
                # pass
                # return [counter]
                table.append({})
                table[counter]['name'] = s.name
                counter = counter + 1

    return table