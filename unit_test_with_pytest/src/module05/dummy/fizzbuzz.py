def fizzbuzz(n, additional_rules=None):
    answer = str()
    rules = {3: "Fizz", 5:"Buzz"}
    additional_rule = {7: "Whizz"}
    if additional_rules:
        rules.update(additional_rule)

    for divisor in sorted(rules.keys()):
        if n % divisor == 0:
            answer += rules[divisor]

    if not answer:
        answer = str(n)

    return answer
