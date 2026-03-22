def test_function(request):
    execution_count = getattr(request.node, 'execution_count', 1)
    if execution_count:
        print(f"当前重试轮数: {execution_count}")
    assert False