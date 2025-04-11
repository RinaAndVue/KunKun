import random

# 从主函数中传入参数
# 传入一个列表对象，为
# 返回一个string对象，作为抽取的名字
# 返回一个bool对象，告知姓名文件是否被更改
# 需要考虑动态概率问题，需要将概率统计存储在本地
def load_name_error(name_list):
    # 检测概率文件是否被更改
    # 读取名字备份目录文件
    try:
        F = open('config\\name.txt',encoding="utf-8")
        line = F.readline().strip()
        name_list_backup = []
        name_list_backup.append(line)
        while line:
            line = F.readline().strip()
            name_list_backup.append(line)
        F.close()
        name_list_backup.pop()
    except:
        name_list_backup = []

    if name_list == name_list_backup:
        print("名单正常，没有发生变化")
        return False
    else:
        print("名单异常，发生变化")
        # 补全文件
        # 默认姓名文件存在
        __backup_file__(name_list)
        return True
        
def __backup_file__(name_list):
    with open("config\\name.txt", 'w', encoding='utf-8') as file:
        for name in name_list:
            file.write(name+'\n')


def __load_dynamical_probability__(name_list):
    try:
        F = open('config\\dynamical_probability.ly',encoding="utf-8")
        line = F.readline().strip()
        dynamical_probability = []
        dynamical_probability.append(int(line))
        while line:
            line = F.readline().strip()
            if line != '':
                dynamical_probability.append(int(line))
        F.close()
        if len(dynamical_probability) != len(name_list):
            raise ValueError('')
        return dynamical_probability
    except ValueError:
        with open("config\\dynamical_probability.ly", 'w', encoding='utf-8') as file:
            for name in name_list:
                file.write('1'+'\n')
        return __load_dynamical_probability__(name_list)
        
def __save_dynamical_probability__(probability_list):
    with open("config\\dynamical_probability.ly", 'w', encoding='utf-8') as file:
        for probability in probability_list:
            file.write(str(probability)+'\n')

def lottery(name_list, weight_size, weight_max):
    probability_list = __load_dynamical_probability__(name_list)
    R_name = []
    # 生成一个临时姓名存储表，用于抽取姓名
    for i in range(0, len(name_list)):
        for r in range(0, int(probability_list[i])):
            R_name.append(name_list[i])
    # 使用随机函数抽取姓名
    name_num = random.randint(0, len(R_name) -1)
    name = R_name[name_num]
    # 增加其它名字的动态概率
    for i in range(0, len(probability_list)):
        if name_list[i] != name and probability_list[i] < len(name_list) * 2 and weight_max == 0:
            probability_list[i] += weight_size
        elif name_list[i] != name and probability_list[i] <= weight_max:
            probability_list[i] += weight_size
        else:
            probability_list[i] = 1
    
    __save_dynamical_probability__(probability_list)
    return name

    
# 测试集
namelist = ['猫咪','小猫','大猫咪','小猫咪','张馨月','cat','dog']
if __name__ == "__main__":
    #lottery(namelist)
    #__load_name_error__(namelist)
    #__load_dynamical_probability__(namelist)
    names = lottery(namelist,1,0)
    print(names)
    #load_name_error(namelist)