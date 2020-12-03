from src.syntactical_analyzer import analise


def test_queries():
    assert analise("connect /dir1/dir2;")
    assert analise("select count edges from graph(/dir3);")
    assert analise("select edges from intersect(graph(/dir4), regex(term(a)*) );")
    assert analise("select edges from intersect(graph(/dir5), regex((term(a) or nonterm(b))?) );")
    assert analise("select edges from regex( (term(a).term(ab)+.nonterm(c)?)* );")
    assert analise("select count edges from graph_with_start_final(set(10, 11, 12), range(1, 5), graph(/dir4));")
    assert analise("a = term(a)*;")
    assert analise("select filter (v, e, u) (e has abc) edges from intersect(graph(/dir4), regex(term(a)*) );")
    assert analise("select filter (v, e, u) ((e has abc and not e has ac)) edges from intersect(graph(/dir4), regex(term(a)*) );")
    assert analise("select filter (v, e, u) ((is_start v or is_final u)) edges from intersect(graph(/dir4), regex(term(a)*) );")
    # all together
    assert analise("connect /dir1/dir2;"
                   "select count edges from graph(/dir6);"
                   "select edges from intersect(regex((term(a)*.term(b)*)), regex((term(a)?.term(b))) );"
                   "a = term(a)*;"
                   "select filter (v, e, u) ((is_start v or is_final u)) edges from intersect(graph(/dir4), regex(nonterm(a)*) );")
    assert not analise("connect /name/")  # no ;
