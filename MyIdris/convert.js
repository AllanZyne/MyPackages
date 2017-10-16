const yaml = require('js-yaml');
const fs   = require('fs');
const util = require('util')



function handleCaptures(p) {
	let o = {};
	// console.log(p)
	for (let i = 0; i <= 100; ++i) {
		let pp = p[i];
		if (pp) {
			o[i] = pp.name;
		}
	}
	return o;
}

function handlePattern(p) {
	var oo = [];

	if (p.match) {
		var o = {};

		o.match = p.match;
		o.scope = p.name;

		oo.push(o);
	}

	if (p.begin) {
		var o = {};

		o.match = p.begin;
		if (p.beginCaptures) {
			o.captures = handleCaptures(p.beginCaptures);
		}

		var push = [];

		push.push({
			meta_scope: p.name
		});

		var end = {
			match: p.end,
			pop: true,
		};

		if (p.endCaptures) {
			end.captures = handleCaptures(p.endCaptures);
		}
		
		push.push(end);

		if (p.patterns) {
			for (let pp of p.patterns) {
				push = push.concat(handlePattern(pp));
			}
		}

		o.push = push;

		oo.push(o);
	}
	
	if (p.include) {
		var o = {};
		o.include = p.include.slice(1);
		oo.push(o);
	}

	if (!p.begin && p.patterns) {
		for (let pp of p.patterns) {
			oo = oo.concat(handlePattern(pp));
		}
	}

	return oo;
}


function converVSCJson(inputFile, outputFile) {
	let content = fs.readFileSync(inputFile, 'utf8');
	let data = JSON.parse(content);

	let sublime_syntax = {
		file_extensions: data.fileTypes,
		scope: data.scopeName,
		contexts: {
		}
	};

	let contexts = sublime_syntax.contexts;

	let main = [];

	for (let pp of data.patterns) {
		let r = handlePattern(pp);
		main = main.concat(r);
	}

	contexts.main = main;

	// console.log(util.inspect(main, false, null))

	for (let name in data.repository) {
		var pp = data.repository[name];
		let r = handlePattern(pp);
		contexts[name] = r;
	}

	// console.log(util.inspect(contexts, false, null))
	let dump = yaml.safeDump(sublime_syntax, {
		lineWidth: 100,
	});

	dump = dump.replace(/^(\s+)'(\d+)':/gm, '$1$2:');

	let dumpHead = '%YAML 1.2\n---\n# vscode-idris\n';

	fs.writeFileSync(outputFile, dumpHead + dump, 'utf8');
}

converVSCJson('./idris.json', './idris.sublime-syntax');
// converVSCJson('./idris.literate.json', './idris.literate.sublime-syntax');
