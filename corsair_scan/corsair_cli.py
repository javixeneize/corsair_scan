import corsair_scan
import click
import json
import sys


def get_data_from_file(filename):
    try:
        with open(filename) as f:
            try:
                data = json.loads(f.read())
                if type(data) == dict:
                    datalist = []
                    datalist.append(data)
                    return datalist
                else:
                    return data
            except json.decoder.JSONDecodeError as e:
                print('Error. The format does not appear to be correct, please review')
                sys.exit(2)
    except FileNotFoundError:
        print('Error. File not found')
        sys.exit(2)


@click.command()
@click.argument('file', required=True)
@click.option('-nv', '--noverify', 'verify', help='Skips security certificate check', is_flag=True, default=True)
@click.option('-r', '--report', 'report', help='Saves the report in a JSON file')
def run_cli_scan(file, verify, report):
    """Corsair CLI requires as parameter a file in JSON format with the data to run the scan.
    This data can be a single request, or a list of requests"""
    data = get_data_from_file(file)
    corsair_report = corsair_scan.corsair_scan(data, verify)
    if corsair_report.get('report'):
        if report:
            with open(report, 'w') as file:
                file.write(json.dumps(corsair_report))
                print("Report generated in {}".format(report))
        else:
            print(corsair_report)
    else:
        print("There was an error running corsair. Please check the input data is correct")


if __name__ == "__main__":
    run_cli_scan()