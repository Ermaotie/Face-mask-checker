import cv2
import json
from aip import AipBodyAnalysis


def get_image():
    cap = cv2.VideoCapture(0)  
    while (1):
        ret, frame = cap.read() 
        cv2.imshow('video', frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("test1.jpg", frame)
            break

    cap.release()
    cv2.destroyAllWindows()


""" 读取图片 """


def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()


# 检测图片
def check_image():
    image = get_file_content('test1.jpg')

    # ID setup
    APP_ID = '19378067'
    API_KEY = 'DAYZeonKGtfLoPXA3UFivyl7'
    SECRET_KEY = 'mGt3Lomozy1G5tueq4Pu1kkQ4xwFhdC'

    client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)

    """ 调用人体关键点识别 """
    keyword = client.bodyAttr(image)
    print(keyword)

    """ 打印json格式 """
    print
    json.dumps(keyword, sort_keys=True, indent=2)

    print("person_num:%d" % (keyword['person_num']))

    draw_image = cv2.imread('test1.jpg')

    for i in range(0, keyword['person_num']):
        # 识别人体的位置（x，y）
        x1 = keyword['person_info'][i]['location']['left']
        y1 = keyword['person_info'][i]['location']['top']

        x2 = keyword['person_info'][i]['location']['width'] + x1
        y2 = keyword['person_info'][i]['location']['height'] + y1

        # 点位取整
        round(x1)
        round(x2)
        round(y1)
        round(y2)

        # 打开图片并绘画出来人体框图
        print("draw_image")

        print("( %d , %d )" % (x1, y1))
        print("( %d , %d )" % (x2, y2))

        # 画出矩形
        cv2.rectangle(draw_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)

        face_mask = keyword['person_info'][i]['attributes']['face_mask']['name']
        mask1 = '无口罩'
        mask2 = '戴口罩'
        mask3 = '不确定'

        if face_mask == mask1:
            mask = "No mask"
        if face_mask == mask2:
            mask = "wear mask"
        if face_mask == mask3:
            mask = "uncertain"

        print(face_mask)
        person_name = 'person' + str(i) + mask
        print(person_name)

        # 标注文本
        cv2.putText(draw_image, person_name, (int(x1), int(y1)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    while (1):
        cv2.imshow('porson_detect', draw_image)  
        if cv2.waitKey(1) & 0xFF == ord('w'):  
            cv2.imwrite("test1.jpg", draw_image)
            break
        if cv2.getWindowProperty('porson_detect', cv2.WND_PROP_AUTOSIZE) < 1:
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    get_image()
    check_image()
