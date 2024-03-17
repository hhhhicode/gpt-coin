import datetime
import json
import schedule
import time
import application.service.my_scheduler as my_scheduler
import application.service.my_upbit as my_upbit
import application.service.my_gpt as my_gpt
import application.service.my_telegram as my_telegram
import utils.file_util as file_util


def make_decision_and_execute():
    result_decision = ""
    print("Making decision and executing...")

    data_json = my_upbit.fetch_and_prepare_data()
    # advice = my_gpt.analyze_data_with_gpt4(data_json)
    #
    # try:
    #     decision = json.loads(advice)
    #     # if decision.get('decision') in ["buy", "strong_buy"]:
    #     #     my_upbit.buy_coin("KRW-BTC", 3800000, 100000*0.9995)
    #     # elif decision.get('decision') == "sell":
    #     #     my_upbit.sell_all_coin("BTC", "KRW-BTC")
    #     print(decision)
    #     my_telegram.send_message(decision)
    #     result_decision = decision
    # except Exception as e:
    #     print(f"Failed to parse the advice as JSON: {e}")

    message = ("JSON Data 1: Market Analysis Data\n" + data_json
               + "\nJSON Data 2: Current Investment State\n" + my_upbit.get_current_status())
    file_util.write_upbit_output(message)

    this_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("DONE WRITING TO FILE: " + this_time)
    my_telegram.send_message("DONE WRITING TO FILE: " + this_time)
    return result_decision


if __name__ == "__main__":
    json_decision = make_decision_and_execute()
    schedule.every().hour.at(":16").do(make_decision_and_execute)

    while True:
        schedule.run_pending()
        time.sleep(1)
