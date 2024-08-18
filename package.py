import os
import json
import logging
import time
import datetime
import filecmp
import shutil

# 常用设置，自行配置
client_name = "GMSE"
use_bandi_zip = True
delete_patch_dir_after_zip = True

# 常用设置，非必要勿动
data_path = os.path.join(os.getcwd(), 'data')
package_path = os.path.join(os.getcwd(), 'package')
package_data_path = os.path.join(package_path, 'data')
update_log_path = os.path.join(data_path, '更新日志.txt')

# 全局变量勿动
old_version = "0.0.0"
patch_file_name = ""

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建一个handler，用于输出到控制台
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
console_handler.setFormatter(console_formatter)

# 创建一个handler，用于输出到文件
file_handler = logging.FileHandler('package.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(file_formatter)

# 将handler添加到logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


def load_version_file():
    with open(os.path.join(os.getcwd(), 'version.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


def save_version_file(json_data):
    with open(os.path.join(os.getcwd(), 'version.json'), 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)


def check_dir():
    return (os.path.exists(data_path)
            and os.path.isdir(data_path)
            and os.path.exists(package_path)
            and os.path.isdir(package_path)
            )


def update_version_info(v_info):
    if v_info['main'] == "" and len(v_info['feat']) == 0 and len(v_info['update']) == 0 and len(v_info['bug']) == 0:
        return False
    global old_version
    old_version = v_info['version']
    f_ver = int(v_info['version'].split('.')[0])
    s_ver = int(v_info['version'].split('.')[1])
    t_ver = int(v_info['version'].split('.')[2])

    if v_info['main'] != "":
        f_ver += 1

    s_ver += len(v_info['feat'])
    s_ver += len(v_info['update'])

    t_ver += len(v_info['bug'])
    new_version = f"{f_ver}.{s_ver}.{t_ver}"
    v_info['version'] = new_version
    logger.info(f"预备版本：{v_info['version']}")
    return True


def read_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""


def output_update_docs(v_info):
    with open(update_log_path, 'w', encoding='utf-8') as f:
        f.write(f"Version: {v_info['version']}")
        if v_info['main'] != "":
            f.write(" ")
            f.write(v_info['main'])
        f.write("\n")
        f.write(f"更新时间 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        f.write("\n")

        if len(v_info['feat']) > 0:
            f.write("功能更新：\n")
            for feat in v_info['feat']:
                f.write(f" - {feat}\n")
        f.write("\n")

        if len(v_info['update']) > 0:
            f.write("其他更新：\n")
            for update in v_info['update']:
                f.write(f" - {update}\n")
        f.write("\n")

        if len(v_info['bug']) > 0:
            f.write("Bug 修复：\n")
            for bug in v_info['bug']:
                f.write(f" - {bug}\n")
        f.write("\n")

        if v_info['comment'] != "":
            f.write("备注：\n")
            f.write(v_info['comment'])


def restore_update_docs(data):
    if data == "":
        os.remove(update_log_path)
    with open(update_log_path, 'w', encoding='utf-8') as f:
        f.write(data)


def compare_and_copy_files(v_info):
    if not os.path.exists(package_data_path):
        os.makedirs(package_data_path)
    if not os.path.isdir(package_data_path):
        logger.error("package/data不是一个目录，请手动删除后再执行")
        exit()

    update_files = 0
    global old_version, patch_file_name
    if old_version != "0.0.0" and old_version != v_info['version']:
        patch_file_name = f"v{old_version}升v{v_info['version']}补丁包"
    elif old_version == v_info['version']:
        logger.info("版本没有发生变化")
        return False
    else:
        logger.info("第一次运行无需生成补丁包")
        return True

    patch_path = os.path.join(package_path, patch_file_name)
    for root, dirs, files in os.walk(data_path):
        data_sub_path = os.path.relpath(root, data_path)
        package_sub_path = os.path.join(package_data_path, data_sub_path)
        patch_sub_path = os.path.join(patch_path, data_sub_path)
        # if gen_patch and not os.path.exists(patch_sub_path):
        #     os.makedirs(patch_sub_path)

        for file in files:
            data_file = os.path.join(root, file)
            package_file = os.path.join(package_sub_path, file)
            patch_file = os.path.join(patch_sub_path, file)

            if not os.path.exists(package_file) or not filecmp.cmp(data_file, package_file, shallow=False):
                if not os.path.exists(patch_sub_path):
                    os.makedirs(patch_sub_path)
                shutil.copy2(data_file, patch_file)
                update_files += 1

    return update_files > 1  # 不算更新日志的情况下


def copy_all_client():
    if os.path.exists(package_data_path):
        shutil.rmtree(package_data_path)
    shutil.copytree(data_path, package_data_path)


if __name__ == '__main__':
    logger.info("==========开始运行脚本==========")
    start_time = time.time()
    version_info = load_version_file()
    logger.info("上次打包版本：" + version_info['version'])

    if not check_dir():
        logger.error("请在脚本的根目录创建data和package文件夹，并将客户端文件放入data目录")
        exit()

    if not update_version_info(version_info):
        logger.warning("版本信息里没有新内容，打包终止")
        exit()

    # 保存原来的更新日志
    old_update_docs_context = read_file(update_log_path)
    # 更新日志
    output_update_docs(version_info)

    logger.info("开始对比文件变化，并生成补丁文件")
    if compare_and_copy_files(version_info):
        logger.info(f"补丁文件已准备完毕：{patch_file_name}")
        logger.info("开始拷贝完整客户端")
        copy_all_client()
        logger.info(f"客户端文件已准备完毕：{package_data_path}")
        version_info['main'] = ""
        version_info['feat'] = []
        version_info['update'] = []
        version_info['bug'] = []
        version_info['comment'] = ""
        save_version_file(version_info)
        if use_bandi_zip:
            logger.info("BandiZip 开始压缩打包客户端")
            zip_path = os.path.join(package_path, f"{client_name}v{version_info['version']}.7z")
            os.system("bz c -l:9 %s %s" % (
                zip_path,
                package_data_path
            ))
            logger.info(f"打包完成：{zip_path}")
            if patch_file_name != "":
                zip_path = os.path.join(package_path, f"{patch_file_name}.7z")
                logger.info("BandiZip 开始压缩打包补丁")
                os.system("bz c -l:9 %s %s" % (
                    zip_path,
                    os.path.join(package_path, patch_file_name)
                ))
                logger.info(f"打包完成：{zip_path}")
                if delete_patch_dir_after_zip:
                    os.remove(os.path.join(package_path, patch_file_name))
                    logger.info("移除补丁目录")

    else:
        logger.warning("当前已是最新版本，没有补丁生成")
        restore_update_docs(old_update_docs_context)

    end_time = time.time()
    elapsed_time = end_time - start_time
    logger.info(f"任务执行完毕，消耗时间 {elapsed_time:.2f} 秒")
